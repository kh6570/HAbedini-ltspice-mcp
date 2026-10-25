# In the name of God, the Most Gracious, the Most Merciful
"""Opt-in LTspice 26 window sync through ltspice-mcp-bridge.

This module speaks to the bridge as a normal MCP client. This module never passes
``--headless`` and never calls ``start_headless`` or ``open_design``. A save
attaches only when ``status`` already shows a GUI the user opened.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator, Callable, Iterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager, contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import anyio
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from ltspice_mcp.adapters.probe import probe_ltspice
from ltspice_mcp.core.exceptions import ValidationError
from ltspice_mcp.infra.call_context import current_settings

_REQUIRED = frozenset(
    {"status", "attach", "list_open_designs", "get_design_content", "set_design_content"}
)
_BLOCKED = frozenset({"start_headless", "open_design"})
_BRIDGE_TIMEOUT_S = 20.0


class BridgeToolsChangedError(Exception):
    """The bridge no longer exposes the tools this sync step needs."""


class BridgeUnavailableError(Exception):
    """The bridge did not answer before this save could verify the open window."""


class DesignBridge(Protocol):
    """This class lists the few bridge tools that window sync can call."""

    def tool_names(self) -> set[str]:
        """Return the tool names the bridge advertised."""

    async def status(self) -> dict[str, object]:
        """Return the bridge status object."""

    async def attach(self, pid: int) -> None:
        """Attach to one LTspice process the user already started."""

    async def list_open_designs(self) -> list[str]:
        """Return paths of documents already open in that window."""

    async def read_design(self, path: str) -> str:
        """Return the text of one open document."""

    async def replace_design(self, path: str, text: str) -> None:
        """Replace one open document in a single undo step."""


@dataclass(frozen=True, slots=True)
class SyncPlan:
    """Whether the save has to push text back into an open window."""

    push: bool
    reason: str


BridgeOpener = Callable[[Path], AsyncIterator[DesignBridge]]


def texts_match(disk_text: str, buffer_text: str) -> bool:
    """Return True when two schematic texts differ only by newline style."""

    return _normalize(disk_text) == _normalize(buffer_text)


def user_gui_pid(status: dict[str, object]) -> int | None:
    """Return the pid of a GUI the user opened.

    The function ignores headless instances and auto-started instances. This function does not
    start LTspice.
    """

    instances = status.get("instances")
    if not isinstance(instances, list):
        return None
    for item in instances:
        if not isinstance(item, dict):
            continue
        mode = str(item.get("mode", "")).lower()
        if "headless" in mode or "gui" not in mode:
            continue
        if item.get("autoStarted") is True or item.get("auto_started") is True:
            continue
        pid = item.get("pid")
        if isinstance(pid, int) and not isinstance(pid, bool) and pid > 0:
            return pid
    return None


def parse_status(text: str) -> dict[str, object]:
    """Parse the JSON object that the bridge ``status`` tool returns."""

    loaded = _json_object(text)
    if loaded is None:
        raise BridgeUnavailableError("The bridge status result was not a JSON object.")
    return loaded


def parse_open_paths(text: str) -> list[str]:
    """Parse ``list_open_designs`` text. One path per line, or a JSON list."""

    stripped = text.strip()
    if not stripped:
        return []
    if stripped.startswith(("[", "{")):
        try:
            loaded = json.loads(stripped)
        except json.JSONDecodeError:
            loaded = None
        if isinstance(loaded, list):
            return [str(item) for item in loaded if str(item).strip()]
        if isinstance(loaded, dict):
            for key in ("designs", "paths", "files"):
                value = loaded.get(key)
                if isinstance(value, list):
                    return [str(item) for item in value if str(item).strip()]
    return [line.strip() for line in stripped.splitlines() if line.strip()]


def parse_design_text(text: str) -> str:
    """Return the document body from ``get_design_content``."""

    loaded = _json_object(text.strip())
    if loaded is not None:
        for key in ("text", "content", "document"):
            value = loaded.get(key)
            if isinstance(value, str):
                return value
    return text


def same_design_path(reported: str, path: Path) -> bool:
    """Return True when a bridge path names ``path``."""

    try:
        return Path(reported).resolve() == path.resolve()
    except OSError:
        return False


async def prepare_window(bridge: DesignBridge, path: Path, disk_text: str) -> SyncPlan:
    """Decide whether this save may push into a window the user already opened."""

    if not _REQUIRED.issubset(bridge.tool_names()):
        raise BridgeToolsChangedError("The bridge tool list no longer includes window sync.")
    pid = user_gui_pid(await bridge.status())
    if pid is None:
        return SyncPlan(push=False, reason="No LTspice window is open.")
    await bridge.attach(pid)
    open_paths = await bridge.list_open_designs()
    if not any(same_design_path(item, path) for item in open_paths):
        return SyncPlan(push=False, reason="That schematic is not open in LTspice.")
    buffer_text = await bridge.read_design(str(path))
    if not texts_match(disk_text, buffer_text):
        raise ValidationError(
            "The open LTspice window differs from the file on disk. "
            "Save the schematic in LTspice, then retry. Nothing was written."
        )
    return SyncPlan(
        push=True,
        reason="Pushed the saved text into the open window as one undo step.",
    )


class _SessionBridge:
    """Adapt one MCP session to ``DesignBridge``."""

    def __init__(self, session: ClientSession, names: set[str]) -> None:
        self._session = session
        self._names = names

    def tool_names(self) -> set[str]:
        return set(self._names)

    async def status(self) -> dict[str, object]:
        return parse_status(await self._text("status", {}))

    async def attach(self, pid: int) -> None:
        await self._text("attach", {"pid": pid})

    async def list_open_designs(self) -> list[str]:
        return parse_open_paths(await self._text("list_open_designs", {}))

    async def read_design(self, path: str) -> str:
        return parse_design_text(await self._text("get_design_content", {"path": path}))

    async def replace_design(self, path: str, text: str) -> None:
        await self._text("set_design_content", {"path": path, "text": text})

    async def _text(self, name: str, arguments: dict[str, object]) -> str:
        if name in _BLOCKED:
            raise BridgeUnavailableError(f"Refusing to call {name}.")
        result = await self._session.call_tool(name, arguments)
        if getattr(result, "isError", False):
            detail = _content_text(result).strip() or name
            raise BridgeUnavailableError(detail)
        return _content_text(result)


@dataclass
class _OpenerSlot:
    """Test hook for the bridge connection. Production leaves ``opener`` unset."""

    opener: Callable[[Path], AbstractAsyncContextManager[DesignBridge]] | None = None


_OPENER = _OpenerSlot()


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def _json_object(text: str) -> dict[str, object] | None:
    if not text.startswith("{"):
        return None
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(loaded, dict):
        return None
    return {str(key): value for key, value in loaded.items()}


def _content_text(result: object) -> str:
    structured = getattr(result, "structuredContent", None)
    if isinstance(structured, dict):
        for key in ("text", "content", "document"):
            value = structured.get(key)
            if isinstance(value, str) and value.strip():
                return value
    chunks: list[str] = []
    content = getattr(result, "content", ())
    if isinstance(content, list | tuple):
        for block in content:
            text = getattr(block, "text", None)
            if isinstance(text, str):
                chunks.append(text)
    return "\n".join(chunks)


def _sync_enabled() -> bool:
    settings = current_settings()
    return settings is not None and settings.window_sync


def run_window_guard(
    path: Path,
    disk_text: str,
    saved_text: str,
    write: Callable[[], str],
) -> tuple[str, dict[str, object] | None]:
    """Write ``path``. Push the new text when an open window matches the disk.

    ``write`` returns the content hash of the bytes it stored. A dirty open
    buffer raises ``ValidationError`` before ``write`` runs.
    """

    if not _sync_enabled():
        return write(), None
    try:
        return asyncio.run(_guard(path, disk_text, saved_text, write))
    except BridgeToolsChangedError:
        return write(), {
            "attached": False,
            "pushed": False,
            "reason": "Bridge tool names changed; saved the file only.",
        }
    except BridgeUnavailableError as exc:
        raise ValidationError(
            "Window sync could not reach the open LTspice window. "
            "Save the schematic in LTspice, then retry. Nothing was written."
        ) from exc


async def _guard(
    path: Path,
    disk_text: str,
    saved_text: str,
    write: Callable[[], str],
) -> tuple[str, dict[str, object]]:
    settings = current_settings()
    if settings is None or not settings.window_sync:
        return write(), {"attached": False, "pushed": False, "reason": "Window sync is off."}
    probe = probe_ltspice(settings)
    executable = probe.bridge_executable
    if not probe.message_bridge or executable is None:
        return write(), {
            "attached": False,
            "pushed": False,
            "reason": "This LTspice build launches the schematic only.",
        }
    opener = _OPENER.opener or _stdio_bridge
    async with opener(executable) as bridge:
        with anyio.fail_after(_BRIDGE_TIMEOUT_S):
            plan = await prepare_window(bridge, path, disk_text)
        digest = write()
        if not plan.push:
            return digest, {"attached": False, "pushed": False, "reason": plan.reason}
        try:
            with anyio.fail_after(_BRIDGE_TIMEOUT_S):
                await bridge.replace_design(str(path), saved_text)
        except (TimeoutError, BridgeUnavailableError):
            return digest, {
                "attached": True,
                "pushed": False,
                "reason": "Saved the file. The open window was not updated.",
            }
        return digest, {"attached": True, "pushed": True, "reason": plan.reason}


@asynccontextmanager
async def _stdio_bridge(executable: Path) -> AsyncIterator[DesignBridge]:
    params = StdioServerParameters(command=str(executable), args=[])
    try:
        async with stdio_client(params) as (read, write):  # noqa: SIM117
            async with ClientSession(read, write) as session:
                with anyio.fail_after(_BRIDGE_TIMEOUT_S):
                    await session.initialize()
                    listed = await session.list_tools()
                names = {tool.name for tool in listed.tools}
                yield _SessionBridge(session, names)
    except TimeoutError as exc:
        raise BridgeUnavailableError("The LTspice bridge timed out.") from exc
    except OSError as exc:
        raise BridgeUnavailableError(str(exc)) from exc


@contextmanager
def use_bridge_opener(
    opener: Callable[[Path], AbstractAsyncContextManager[DesignBridge]],
) -> Iterator[None]:
    """Install a bridge opener for one test."""

    previous = _OPENER.opener
    _OPENER.opener = opener
    try:
        yield
    finally:
        _OPENER.opener = previous
