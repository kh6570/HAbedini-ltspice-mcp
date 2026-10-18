# In the name of God, the Most Gracious, the Most Merciful
"""Measure avg, rms, max, min, pp, or peak."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="measure_waveform",
    title="Measure Waveform",
    summary="Measure avg, rms, max, min, pp, or peak.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
