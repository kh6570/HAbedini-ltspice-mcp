# In the name of God, the Most Gracious, the Most Merciful
"""Read the Fourier section of a log."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="read_fourier",
    title="Read Fourier",
    summary="Read the Fourier section of a log.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
