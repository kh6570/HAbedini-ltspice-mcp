# In the name of God, the Most Gracious, the Most Merciful
"""Return primitive pin-to-net connectivity."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="read_net_connectivity",
    title="Read Net Connectivity",
    summary="Return primitive pin-to-net connectivity.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
