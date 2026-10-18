# In the name of God, the Most Gracious, the Most Merciful
"""Keep operating-point rows whose name contains ``device``."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="filter_device_operating_points",
    title="Filter Device Operating Points",
    summary="Keep operating-point rows whose name contains ``device``.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
