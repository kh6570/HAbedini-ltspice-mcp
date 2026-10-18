# In the name of God, the Most Gracious, the Most Merciful
"""Bode magnitude and phase of output/reference."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="measure_bode_response",
    title="Measure Bode Response",
    summary="Bode magnitude and phase of output/reference.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
