# In the name of God, the Most Gracious, the Most Merciful
"""Set a component value."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="set_component_value",
    title="Set Component Value",
    summary="Set a component value.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
