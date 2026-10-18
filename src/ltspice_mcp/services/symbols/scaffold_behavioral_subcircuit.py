# In the name of God, the Most Gracious, the Most Merciful
"""Write a schematic whose only active device is a behavioral source."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="scaffold_behavioral_subcircuit",
    title="Scaffold Behavioral Subcircuit",
    summary="Write a schematic whose only active device is a behavioral source.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
