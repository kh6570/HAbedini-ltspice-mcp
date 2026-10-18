# In the name of God, the Most Gracious, the Most Merciful
"""Move a component and wires that ended on its pins."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="set_component_position",
    title="Set Component Position",
    summary="Move a component and wires that ended on its pins.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
