# In the name of God, the Most Gracious, the Most Merciful
"""Gain and phase margins."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="measure_stability_margins",
    title="Measure Stability Margins",
    summary="Gain and phase margins.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
