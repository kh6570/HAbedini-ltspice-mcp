# In the name of God, the Most Gracious, the Most Merciful
"""This module reports environment readiness for the ``--setup`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ltspice_mcp.adapters.probe import build_summary

if TYPE_CHECKING:
    from ltspice_mcp.infra.config import LTspiceSettings


def describe_environment_readiness(settings: LTspiceSettings) -> dict[str, object]:
    """Return a JSON-serializable readiness report for first-time setup."""

    effective = settings.normalized()
    ltspice = build_summary(effective)
    workspace_root = effective.workspace_root
    exists = workspace_root.is_dir()
    ready = bool(ltspice["exists"]) and exists
    return {
        "ready": ready,
        "ltspice": ltspice,
        "workspace": {
            "path": str(workspace_root),
            "exists": exists,
            "writable": exists,
        },
        "mixed_signal": {
            "dll_devices": False,
            "note": "LTspice has no C++ DLL, Verilog, or socket custom-device toolchain.",
        },
        "transport": effective.transport,
        "enable_sse": effective.enable_sse,
        "log_folder": str(effective.log_folder) if effective.log_folder is not None else None,
        "recipe_path": str(effective.recipe_path) if effective.recipe_path is not None else None,
    }


__all__ = ["describe_environment_readiness"]
