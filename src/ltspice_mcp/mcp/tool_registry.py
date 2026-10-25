# In the name of God, the Most Gracious, the Most Merciful
"""Tool definition registry for the MCP layer."""

from __future__ import annotations

from dataclasses import replace
from functools import cache
from typing import TYPE_CHECKING

from mcp_app_core.registry import ToolAnnotations, implemented_tools
from mcp_app_core.registry import ToolDefinition as CoreToolDefinition
from mcp_app_core.registry import build_tool_registry as build_core_tool_registry

from ltspice_mcp.services._internals.service_catalog import build_service_spec_catalog
from ltspice_mcp.services.service_spec import ServiceSpec

if TYPE_CHECKING:
    from collections.abc import Collection

_DESCRIBE = ServiceSpec(
    name="describe_server_capabilities",
    title="Describe Server Capabilities",
    summary="Report server-level backend availability and feature flags.",
    phase="implemented",
)
_DEFAULT_PROFILES = ("default",)
_HASH_PROPERTY: dict[str, object] = {
    "type": "string",
    "description": (
        "SHA-256 hex digest of this schematic from the last read. "
        "Required when the file already exists. A mismatch writes nothing."
    ),
}
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

ToolDefinition = CoreToolDefinition

__all__ = [
    "ToolAnnotations",
    "ToolDefinition",
    "build_runtime_tool_registry",
    "build_tool_registry",
]


@cache
def _load_specs() -> tuple[ServiceSpec, ...]:
    return build_service_spec_catalog(extra_specs=(_DESCRIBE,))


def _with_expected_hash(tool: CoreToolDefinition) -> CoreToolDefinition:
    if tool.service.read_only:
        return tool
    properties = tool.input_schema.get("properties")
    if not isinstance(properties, dict):
        return tool
    if "schematic_path" not in properties and "destination_path" not in properties:
        return tool
    updated = dict(properties)
    updated["expected_hash"] = dict(_HASH_PROPERTY)
    schema = dict(tool.input_schema)
    schema["properties"] = updated
    return replace(tool, input_schema=schema)


def build_tool_registry(
    service_specs: tuple[ServiceSpec, ...] | None = None,
    *,
    active_profiles: Collection[str] | None = _DEFAULT_PROFILES,
) -> tuple[CoreToolDefinition, ...]:
    """Build the tool registry from the service catalog.

    A normal session passes ``("default",)``. Pass ``None`` to include every
    profile. Extended tools stay out until ``active_profiles`` names ``extended``.
    """

    specs = service_specs or _load_specs()
    tools = build_core_tool_registry(
        specs,
        open_world_names=_OPEN_WORLD,
        active_profiles=active_profiles,
    )
    return tuple(_with_expected_hash(tool) for tool in tools)


def build_runtime_tool_registry(
    tool_definitions: tuple[CoreToolDefinition, ...] | None = None,
    *,
    active_profiles: Collection[str] | None = _DEFAULT_PROFILES,
) -> tuple[CoreToolDefinition, ...]:
    """Return tools when the server implements their services."""

    definitions = (
        tool_definitions
        if tool_definitions is not None
        else build_tool_registry(active_profiles=active_profiles)
    )
    return implemented_tools(definitions)
