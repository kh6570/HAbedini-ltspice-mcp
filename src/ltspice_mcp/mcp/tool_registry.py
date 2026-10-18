# In the name of God, the Most Gracious, the Most Merciful
"""Tool definition registry for the MCP layer."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache

from ltspice_mcp.services._internals.service_catalog import build_service_spec_catalog
from ltspice_mcp.services.service_spec import ServiceSpec

_DESCRIBE = ServiceSpec(
    name="describe_server_capabilities",
    title="Describe Server Capabilities",
    summary="Report server-level backend availability and feature flags.",
    phase="implemented",
)

_OPEN_WORLD = frozenset(
    {
        "run_simulation",
        "run_monte_carlo",
        "run_model_sweep",
        "run_param_sweep",
        "run_value_sweep",
        "run_worst_case",
        "submit_batch",
        "submit_remote_simulation",
        "open_schematic_in_gui",
        "write_workspace_text_file",
    }
)


@dataclass(frozen=True, slots=True)
class ToolAnnotations:
    """Behavior hints for MCP clients."""

    read_only_hint: bool = False
    destructive_hint: bool = False
    idempotent_hint: bool = False
    open_world_hint: bool = False


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    """Metadata for one MCP tool."""

    name: str
    title: str
    description: str
    input_schema: dict[str, object]
    annotations: ToolAnnotations
    service: ServiceSpec

    def summary(self) -> dict[str, object]:
        """Return a JSON-serializable summary."""

        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "read_only": self.annotations.read_only_hint,
            "long_running": self.service.long_running,
        }


def resolve_tool_annotations(spec: ServiceSpec) -> ToolAnnotations:
    """Derive MCP annotation hints from a service spec."""

    return ToolAnnotations(
        read_only_hint=spec.read_only,
        destructive_hint=spec.destructive,
        idempotent_hint=spec.idempotent if spec.idempotent is not None else spec.read_only,
        open_world_hint=spec.long_running or spec.name in _OPEN_WORLD,
    )


_WORKSPACE_PROPERTY: dict[str, object] = {
    "type": "string",
    "description": "Optional per-call workspace root override.",
}


def _normalize_schema(input_schema: dict[str, object]) -> dict[str, object]:
    schema = dict(input_schema)
    existing = schema.get("properties", {})
    properties: dict[str, object] = dict(existing) if isinstance(existing, dict) else {}
    path_like = any(
        name.endswith(("_path", "_dir", "_file", "_root")) or name in {"path", "dir", "file"}
        for name in properties
    )
    if path_like and "workspace_root" not in properties:
        properties["workspace_root"] = dict(_WORKSPACE_PROPERTY)
    schema["properties"] = properties
    schema.setdefault("required", [])
    return schema


@cache
def _load_specs() -> tuple[ServiceSpec, ...]:
    return build_service_spec_catalog(extra_specs=(_DESCRIBE,))


def build_tool_registry(
    service_specs: tuple[ServiceSpec, ...] | None = None,
) -> tuple[ToolDefinition, ...]:
    """Build the tool registry from the service catalog."""

    specs = service_specs or _load_specs()
    tools: list[ToolDefinition] = []
    for spec in specs:
        if spec.input_schema is None:
            raise KeyError(f"Missing MCP input_schema for service {spec.name!r}.")
        tools.append(
            ToolDefinition(
                name=spec.name,
                title=spec.title,
                description=spec.description or spec.summary,
                input_schema=_normalize_schema(dict(spec.input_schema)),
                annotations=resolve_tool_annotations(spec),
                service=spec,
            )
        )
    return tuple(tools)


def build_runtime_tool_registry(
    tool_definitions: tuple[ToolDefinition, ...] | None = None,
) -> tuple[ToolDefinition, ...]:
    """Return tools whose services are implemented."""

    definitions = tool_definitions or build_tool_registry()
    return tuple(tool for tool in definitions if tool.service.phase == "implemented")
