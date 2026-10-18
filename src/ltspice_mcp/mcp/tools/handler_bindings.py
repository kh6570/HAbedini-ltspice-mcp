# In the name of God, the Most Gracious, the Most Merciful
"""Bind catalog callables to MCP handlers."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING

from ltspice_mcp.mcp.capabilities import describe_server_capabilities
from ltspice_mcp.services._internals.service_catalog import build_service_callable_catalog

if TYPE_CHECKING:
    from ltspice_mcp.infra.config import LTspiceSettings
    from ltspice_mcp.mcp.tool_registry import ToolDefinition

    from .runtime import LTspiceToolRuntime

ToolHandler = Callable[..., dict[str, object]]


def _jsonify(value: object) -> object:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonify(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonify(item) for item in value]
    if isinstance(value, float | int | str | bool) or value is None:
        return value
    return str(value)


def to_json_object(value: object) -> dict[str, object]:
    """Require a mapping and coerce nested values into JSON types."""

    if not isinstance(value, dict):
        raise TypeError("Tool handlers must return a dictionary.")
    return {str(key): _jsonify(item) for key, item in value.items()}


def _call_kwargs(
    runtime: LTspiceToolRuntime,
    service_fn: Callable[..., object],
    tool_kwargs: dict[str, object],
    settings: LTspiceSettings,
) -> dict[str, object]:
    call_kwargs: dict[str, object] = {}
    for name, parameter in inspect.signature(service_fn).parameters.items():
        if name == "workspace_root":
            call_kwargs[name] = settings.workspace_root
        elif name == "settings":
            call_kwargs[name] = settings
        elif name == "ltspice_executable":
            call_kwargs[name] = settings.exe
        elif name in tool_kwargs:
            call_kwargs[name] = tool_kwargs[name]
        elif parameter.default is inspect.Parameter.empty:
            raise TypeError(f"Missing required tool argument {name!r}.")
    return call_kwargs


def _effective_settings(runtime: LTspiceToolRuntime, kwargs: dict[str, object]) -> LTspiceSettings:
    override = kwargs.pop("workspace_root", None)
    if override is None or override == "":
        return runtime.settings
    return runtime.settings.model_copy(update={"workspace_root": Path(str(override))}).normalized()


def build_handler(runtime: LTspiceToolRuntime, tool: ToolDefinition) -> ToolHandler:
    """Return the handler for one tool."""

    if tool.name == "describe_server_capabilities":

        def describe() -> dict[str, object]:
            return to_json_object(
                describe_server_capabilities(settings=runtime.settings, tools=runtime.tools)
            )

        describe.__name__ = tool.name
        return describe

    catalog = build_service_callable_catalog()

    def handler(**kwargs: object) -> dict[str, object]:
        service_fn = catalog[tool.name]
        if not callable(service_fn):
            raise TypeError(f"{tool.name} is not callable.")
        settings = _effective_settings(runtime, kwargs)
        if "extra_switches" in kwargs and isinstance(kwargs["extra_switches"], list):
            kwargs["extra_switches"] = tuple(str(item) for item in kwargs["extra_switches"])
        return to_json_object(service_fn(**_call_kwargs(runtime, service_fn, kwargs, settings)))

    handler.__name__ = tool.name
    return handler
