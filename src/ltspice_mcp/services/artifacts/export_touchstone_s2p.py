# In the name of God, the Most Gracious, the Most Merciful
"""Write a one-port-style S2P using S21 = output/reference and the other terms at 0."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="export_touchstone_s2p",
    title="Export Touchstone S2p",
    summary="Write a one-port-style S2P using S21 = output/reference and the other terms at 0.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
