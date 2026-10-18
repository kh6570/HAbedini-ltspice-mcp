# In the name of God, the Most Gracious, the Most Merciful
"""FastMCP server bootstrap."""

from __future__ import annotations

import json
from contextlib import suppress
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, cast

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.shared.exceptions import McpError
from mcp.types import ContentBlock, ErrorData
from mcp.types import ToolAnnotations as MCPToolAnnotations

from ltspice_mcp.adapters import describe_adapters, select_adapter
from ltspice_mcp.adapters.probe import ProbeResult, probe_ltspice
from ltspice_mcp.core.exceptions import (
    AdapterNotFoundError,
    LTspiceError,
    ParseError,
    SimulationError,
    ValidationError,
)
from ltspice_mcp.infra.config import LTspiceSettings, build_settings
from ltspice_mcp.infra.logging import get_logger
from ltspice_mcp.mcp.definition import ServerDefinition, build_server_definition
from ltspice_mcp.mcp.prompts import get_prompt_definitions
from ltspice_mcp.mcp.resources import (
    ResourceDefinition,
    get_resource_content,
    get_resource_definitions,
)
from ltspice_mcp.mcp.tool_registry import (
    ToolAnnotations,
    ToolDefinition,
    build_runtime_tool_registry,
    build_tool_registry,
)
from ltspice_mcp.mcp.tools.runtime import LTspiceToolRuntime

if TYPE_CHECKING:
    from collections.abc import Callable

_ERROR_CODE = 0


def _log_level(
    level: Literal["debug", "info", "warning", "error"],
) -> Literal["DEBUG", "INFO", "WARNING", "ERROR"]:
    if level == "debug":
        return "DEBUG"
    if level == "info":
        return "INFO"
    if level == "warning":
        return "WARNING"
    return "ERROR"


def _annotations(annotations: ToolAnnotations) -> MCPToolAnnotations:
    return MCPToolAnnotations(
        readOnlyHint=annotations.read_only_hint,
        destructiveHint=annotations.destructive_hint,
        idempotentHint=annotations.idempotent_hint,
        openWorldHint=annotations.open_world_hint,
    )


def _error_data(error: LTspiceError) -> ErrorData:
    data: dict[str, object] = {
        "error_code": error.error_code,
        "error_type": type(error).__name__,
    }
    if isinstance(error, SimulationError):
        if error.exit_code is not None:
            data["exit_code"] = error.exit_code
        if error.stderr is not None:
            data["stderr"] = error.stderr
    if isinstance(error, ParseError):
        if error.line is not None:
            data["line"] = error.line
        if error.column is not None:
            data["column"] = error.column
    return ErrorData(code=_ERROR_CODE, message=str(error), data=data)


class _LTspiceFastMCP(FastMCP):
    """FastMCP variant that preserves structured LTspice errors."""

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> list[ContentBlock] | dict[str, Any]:
        tool = self._tool_manager.get_tool(name)
        if tool is None:
            raise ToolError(f"Unknown tool: {name}")
        try:
            result = await tool.fn_metadata.call_fn_with_arg_validation(
                tool.fn,
                tool.is_async,
                dict(arguments),
                None,
            )
            return cast(
                "list[ContentBlock] | dict[str, Any]",
                tool.fn_metadata.convert_result(result),
            )
        except McpError:
            raise
        except LTspiceError as exc:
            raise McpError(_error_data(exc)) from exc
        except ValueError as exc:
            raise McpError(_error_data(ValidationError(str(exc)))) from exc
        except Exception as exc:
            raise ToolError(f"Error executing tool {name}: {exc}") from exc


def _register_resources(app: FastMCP, resources: tuple[ResourceDefinition, ...]) -> None:
    def make_resource(body: str) -> Callable[[], str]:
        def resource() -> str:
            return body

        return resource

    for resource in resources:
        body = get_resource_content(resource.uri) or resource.description
        app.resource(
            resource.uri,
            name=resource.name,
            title=resource.name,
            description=resource.description,
            mime_type=resource.mime_type,
        )(make_resource(body))


def _register_prompts(app: FastMCP) -> None:
    def make_prompt(body: str) -> Callable[[], str]:
        def prompt() -> str:
            return body

        return prompt

    for prompt in get_prompt_definitions():
        app.prompt(prompt.name, description=prompt.description)(make_prompt(prompt.body))


@dataclass(frozen=True, slots=True)
class LTspiceMCPServer:
    """Bootstrapped server metadata and runtime registrations."""

    definition: ServerDefinition
    settings: LTspiceSettings
    tools: tuple[ToolDefinition, ...]
    registered_tools: tuple[ToolDefinition, ...]
    resources: tuple[ResourceDefinition, ...]
    probe: ProbeResult
    tool_runtime: LTspiceToolRuntime
    app: FastMCP

    def summary(self) -> dict[str, object]:
        """Return a JSON-serializable bootstrap summary."""

        return {
            "name": self.definition.name,
            "title": self.definition.title,
            "engine": "ltspice",
            "features": self.definition.features.model_dump(),
            "parameters": [parameter.name for parameter in self.definition.parameters],
            "settings": {
                "transport": self.settings.transport,
                "workspace_root": str(self.settings.workspace_root),
                "cache_dir": str(self.settings.cache_dir),
                "log_level": self.settings.log_level,
                "timeout_s": self.settings.timeout_s,
            },
            "probe": self.probe.summary(),
            "tools": [tool.summary() for tool in self.tools],
            "registered_tools": [tool.name for tool in self.registered_tools],
            "resources": [resource.uri for resource in self.resources],
        }

    def invoke_tool(self, name: str, /, **kwargs: object) -> dict[str, object]:
        """Invoke one bound tool handler directly."""

        return self.tool_runtime.invoke(name, **kwargs)


def _build_app(
    definition: ServerDefinition,
    settings: LTspiceSettings,
    resources: tuple[ResourceDefinition, ...],
    registered_tools: tuple[ToolDefinition, ...],
    runtime: LTspiceToolRuntime,
) -> FastMCP:
    app = _LTspiceFastMCP(
        definition.title,
        instructions=definition.instructions,
        log_level=_log_level(settings.log_level),
    )
    for tool in registered_tools:
        app.tool(
            name=tool.name,
            title=tool.title,
            description=tool.description,
            annotations=_annotations(tool.annotations),
            structured_output=False,
        )(runtime.get_handler(tool.name))
        registered = app._tool_manager.get_tool(tool.name)
        if registered is not None:
            registered.parameters = dict(tool.input_schema)
    _register_resources(app, resources)
    _register_prompts(app)
    return app


def create_server(settings: LTspiceSettings | None = None) -> LTspiceMCPServer:
    """Create the FastMCP server from the current settings."""

    effective = settings.normalized() if settings is not None else build_settings()
    probe = probe_ltspice(effective)
    if effective.exe is None and probe.executable is not None and probe.exists:
        effective = effective.model_copy(update={"exe": probe.executable}).normalized()
    with suppress(AdapterNotFoundError):
        select_adapter(probe)
    describe_adapters(probe)
    definition = build_server_definition()
    tools = build_tool_registry()
    registered = build_runtime_tool_registry(tools)
    resources = get_resource_definitions()
    runtime = LTspiceToolRuntime(effective, registered)
    missing = [tool.name for tool in registered if tool.name not in runtime._handlers]
    if missing:
        raise RuntimeError(f"Missing handlers: {', '.join(missing)}")
    return LTspiceMCPServer(
        definition=definition,
        settings=effective,
        tools=tools,
        registered_tools=registered,
        resources=resources,
        probe=probe,
        tool_runtime=runtime,
        app=_build_app(definition, effective, resources, registered, runtime),
    )


def run(*, settings: LTspiceSettings | None = None, describe: bool = False) -> int:
    """Run the MCP server or print a bootstrap summary."""

    server = create_server(settings)
    logger = get_logger(component="mcp.server")
    logger.info(
        "server_bootstrap_ready",
        tool_count=len(server.registered_tools),
        ltspice_available=server.probe.exists,
    )
    if describe:
        print(json.dumps(server.summary(), indent=2))
        return 0
    server.app.run(transport=server.settings.transport)
    return 0
