# In the name of God, the Most Gracious, the Most Merciful
"""Add a net label."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_net_label",
    title="Add Net Label",
    summary="Add a net label.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
