# In the name of God, the Most Gracious, the Most Merciful
"""The capability report that describe_server_capabilities returns."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from ltspice_mcp.adapters.probe import probe_ltspice
from ltspice_mcp.core.error_taxonomy import error_code_catalog
from ltspice_mcp.services._internals.service_catalog import (
    EXTENDED_GROUP_PACKAGES,
    discover_package_service_specs,
)

_ENABLE_EXTENDED = (
    "Set LTSPICE_ACTIVE_PROFILES=default,extended or start the server with "
    "--active-profiles default,extended."
)

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
    loaded = {tool.name for tool in tools}
    groups = Counter(tool.service.name.split("_")[0] for tool in tools)
    hidden = _hidden_groups(loaded)
    return {
        "engine": "ltspice",
        "source_of_truth": ".asc",
        "derived": [".net", ".log", ".raw"],
        "probe": probe.summary(),
        "tool_count": len(tools),
        "tools": [tool.name for tool in tools],
        "name_prefixes": dict(groups),
        "active_profiles": list(settings.active_profile_names()),
        "hidden_groups": hidden,
        "extended_profiles": {
            "loaded": "extended" in settings.active_profile_names(),
            "enable": _ENABLE_EXTENDED,
        },
        "features": {
            "schematic_inspection": True,
            "waveform_parsing": True,
            "simulation": True,
            "dll_devices": False,
            "gui_command_channel": probe.message_bridge,
        },
        "error_codes": error_code_catalog(),
        "limits": {"max_points": 2000, "max_bytes": 64000},
    }


def _hidden_groups(loaded: set[str]) -> list[dict[str, object]]:
    hidden: list[dict[str, object]] = []
    for label, package in EXTENDED_GROUP_PACKAGES.items():
        names = [
            spec.name
            for spec in discover_package_service_specs(package)
            if spec.phase == "implemented" and spec.name not in loaded
        ]
        if not names:
            continue
        hidden.append(
            {
                "group": label,
                "profile": "extended",
                "tools": names,
                "enable": _ENABLE_EXTENDED,
            }
        )
    return hidden
