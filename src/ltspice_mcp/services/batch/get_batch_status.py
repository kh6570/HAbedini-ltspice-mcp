# In the name of God, the Most Gracious, the Most Merciful
"""Return a batch manifest summary."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="get_batch_status",
    title="Get Batch Status",
    summary="Return a batch manifest summary.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
