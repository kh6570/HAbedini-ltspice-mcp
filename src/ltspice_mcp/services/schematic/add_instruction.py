# In the name of God, the Most Gracious, the Most Merciful
"""Add a SPICE directive or a comment."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_instruction",
    title="Add Instruction",
    summary="Add a SPICE directive or a comment.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
