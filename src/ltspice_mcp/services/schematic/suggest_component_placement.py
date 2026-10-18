# In the name of God, the Most Gracious, the Most Merciful
"""Suggest the next free grid point to the right of existing parts."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="suggest_component_placement",
    title="Suggest Component Placement",
    summary="Suggest the next free grid point to the right of existing parts.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
