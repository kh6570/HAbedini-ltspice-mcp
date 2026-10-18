# In the name of God, the Most Gracious, the Most Merciful
"""Evaluate an expression built from raw signal names."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="evaluate_waveform_expression",
    title="Evaluate Waveform Expression",
    summary="Evaluate an expression built from raw signal names.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
