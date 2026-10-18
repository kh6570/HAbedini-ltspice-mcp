# In the name of God, the Most Gracious, the Most Merciful
"""Read one budgeted waveform."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="read_waveform",
    title="Read Waveform",
    summary="Read one budgeted waveform.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
