# In the name of God, the Most Gracious, the Most Merciful
"""Mark a batch cancelled. A finished batch stays completed."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="cancel_batch",
    title="Cancel Batch",
    summary="Mark a batch cancelled. A finished batch stays completed.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=True,
    idempotent=False,
)
