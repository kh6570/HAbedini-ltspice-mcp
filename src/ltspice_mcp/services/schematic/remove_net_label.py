# In the name of God, the Most Gracious, the Most Merciful
"""Remove a net label."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="remove_net_label",
    title="Remove Net Label",
    summary="Remove a net label.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=True,
    idempotent=False,
)
