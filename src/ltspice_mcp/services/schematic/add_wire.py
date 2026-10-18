# In the name of God, the Most Gracious, the Most Merciful
"""Add a wire. Exposed as ``add_wire`` by the tool module."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_wire",
    title="Add Wire",
    summary="Add a wire. Exposed as ``add_wire`` by the tool module.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
