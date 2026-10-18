# In the name of God, the Most Gracious, the Most Merciful
"""Set a value on a component inside a schematic subcircuit file."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="set_subcircuit_component_value",
    title="Set Subcircuit Component Value",
    summary="Set a value on a component inside a schematic subcircuit file.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
