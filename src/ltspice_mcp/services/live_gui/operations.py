# In the name of God, the Most Gracious, the Most Merciful
"""Launch the LTspice GUI. There is no command channel into the window."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from ltspice_mcp.adapters.probe import probe_ltspice
from ltspice_mcp.core.exceptions import BackendUnavailableError, UnsupportedError
from ltspice_mcp.services._shared.paths import validate_existing_file

if TYPE_CHECKING:
    from pathlib import Path

    from ltspice_mcp.infra.config import LTspiceSettings

_PROCESSES: dict[str, subprocess.Popen[bytes]] = {}


def describe_live_gui_support(*, workspace_root: Path) -> dict[str, object]:
    """Describe the GUI launch support."""

    del workspace_root
    return {
        "open_schematic": True,
        "command_channel": False,
        "note": "LTspice can be launched on an .asc file. It has no message bridge.",
    }


def _unsupported(action: str) -> dict[str, object]:
    raise UnsupportedError(
        f"{action} is unavailable. LTspice has no GUI automation channel. "
        "Open the schematic, edit the .asc, and run a batch simulation instead."
    )


def open_schematic_in_gui(
    *,
    workspace_root: Path,
    schematic_path: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Launch LTspice on a schematic without ``-b``."""

    path = validate_existing_file(schematic_path, workspace_root=workspace_root, suffixes=(".asc",))
    exe = ltspice_executable
    if exe is None or not exe.is_file():
        if settings is None:
            raise BackendUnavailableError("LTspice settings were not provided.")
        probed = probe_ltspice(settings)
        exe = probed.executable if probed.exists else None
    if exe is None:
        raise BackendUnavailableError("LTspice is not installed.")
    process = subprocess.Popen([str(exe), str(path)])  # noqa: S603
    _PROCESSES[str(path)] = process
    return {"pid": process.pid, "path": str(path)}


def close_live_gui_session(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Stop a GUI process this server launched."""

    path = validate_existing_file(schematic_path, workspace_root=workspace_root, suffixes=(".asc",))
    process = _PROCESSES.pop(str(path), None)
    if process is None or process.poll() is not None:
        return {"closed": False, "reason": "No GUI process is tracked for that schematic."}
    process.terminate()
    return {"closed": True, "pid": process.pid}


def refresh_schematic_in_gui(
    *,
    workspace_root: Path,
    schematic_path: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Close and reopen the schematic so the GUI reloads the file."""

    close_live_gui_session(workspace_root=workspace_root, schematic_path=schematic_path)
    return open_schematic_in_gui(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        settings=settings,
        ltspice_executable=ltspice_executable,
    )


def poll_live_gui_session(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Report that polling a GUI session is unsupported."""

    del workspace_root, schematic_path
    return _unsupported("poll_live_gui_session")


def poll_live_gui_session_events(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Report that GUI events are unsupported."""

    del workspace_root, schematic_path
    return _unsupported("poll_live_gui_session_events")


def send_live_gui_session_command(
    *, workspace_root: Path, schematic_path: str, command: str
) -> dict[str, object]:
    """Report that GUI commands are unsupported."""

    del workspace_root, schematic_path, command
    return _unsupported("send_live_gui_session_command")
