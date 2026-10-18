# In the name of God, the Most Gracious, the Most Merciful
"""Compare the means of one signal in two raw files."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="compare_waveforms",
    title="Compare Waveforms",
    summary="Compare the means of one signal in two raw files.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
