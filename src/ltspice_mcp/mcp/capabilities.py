# In the name of God, the Most Gracious, the Most Merciful
"""Capability report returned by describe_server_capabilities."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from ltspice_mcp.adapters.probe import probe_ltspice
from ltspice_mcp.core.error_taxonomy import error_code_catalog

if TYPE_CHECKING:
    from ltspice_mcp.infra.config import LTspiceSettings
    from ltspice_mcp.mcp.tool_registry import ToolDefinition


def describe_server_capabilities(
    *,
    settings: LTspiceSettings,
    tools: tuple[ToolDefinition, ...],
) -> dict[str, object]:
    """Report the engine, probe result, and registered tools."""

    probe = probe_ltspice(settings)
    groups = Counter(tool.service.name.split("_")[0] for tool in tools)
    return {
        "engine": "ltspice",
        "source_of_truth": ".asc",
        "derived": [".net", ".log", ".raw"],
        "probe": probe.summary(),
        "tool_count": len(tools),
        "tools": [tool.name for tool in tools],
        "name_prefixes": dict(groups),
        "features": {
            "schematic_inspection": True,
            "waveform_parsing": True,
            "simulation": True,
            "dll_devices": False,
            "gui_command_channel": False,
        },
        "error_codes": error_code_catalog(),
        "limits": {"max_points": 2000, "max_bytes": 64000},
    }
