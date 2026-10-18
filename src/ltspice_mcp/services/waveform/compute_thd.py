# In the name of God, the Most Gracious, the Most Merciful
"""Total harmonic distortion."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="compute_thd",
    title="Compute Thd",
    summary="Total harmonic distortion.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
