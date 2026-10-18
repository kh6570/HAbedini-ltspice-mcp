# In the name of God, the Most Gracious, the Most Merciful
"""Split a wire so a coordinate becomes a junction."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_junction",
    title="Add Junction",
    summary="Split a wire so a coordinate becomes a junction.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
