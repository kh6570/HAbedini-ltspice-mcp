# In the name of God, the Most Gracious, the Most Merciful
"""Return the stored batch result."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="collect_batch_results",
    title="Collect Batch Results",
    summary="Return the stored batch result.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
