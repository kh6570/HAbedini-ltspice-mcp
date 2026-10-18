# In the name of God, the Most Gracious, the Most Merciful
"""Set SpiceLine attributes."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="set_component_parameters",
    title="Set Component Parameters",
    summary="Set SpiceLine attributes.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
