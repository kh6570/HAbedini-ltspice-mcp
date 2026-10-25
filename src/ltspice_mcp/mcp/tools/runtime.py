# In the name of God, the Most Gracious, the Most Merciful
"""Per-server tool runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import anyio

from ltspice_mcp.mcp.tools.handler_bindings import ToolHandler, build_handler
from ltspice_mcp.mcp.tools.schema_handlers import expose_tool_schema

if TYPE_CHECKING:
    from collections.abc import Callable

    from ltspice_mcp.infra.config import LTspiceSettings
    from ltspice_mcp.mcp.tool_registry import ToolDefinition


@dataclass
class LTspiceToolRuntime:
    """Bound handlers for one server instance."""

    settings: LTspiceSettings
    tools: tuple[ToolDefinition, ...]
    _handlers: dict[str, ToolHandler] = field(init=False)

    def __post_init__(self) -> None:
        self._handlers = {}
        for tool in self.tools:
            self._handlers[tool.name] = expose_tool_schema(build_handler(self, tool), tool)

    def get_handler(self, name: str) -> Callable[..., object]:
        """Return one handler. Use a thread when the tool takes a long time."""

        handler = self._handlers[name]
        tool = next(item for item in self.tools if item.name == name)
        if tool.service.long_running:
            return _threaded(handler, name)
        return handler

    def invoke(self, name: str, /, **kwargs: object) -> dict[str, object]:
        """Call one handler from tests or local code."""

        return self._handlers[name](**kwargs)


def _threaded(handler: ToolHandler, name: str) -> Callable[..., object]:
    async def async_handler(**kwargs: object) -> dict[str, object]:
        return await anyio.to_thread.run_sync(lambda: handler(**kwargs))

    async_handler.__name__ = name
    async_handler.__signature__ = handler.__signature__  # type: ignore[attr-defined]
    return async_handler
