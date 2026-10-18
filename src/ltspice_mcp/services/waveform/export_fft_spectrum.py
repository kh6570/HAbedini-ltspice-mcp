# In the name of God, the Most Gracious, the Most Merciful
"""Write an FFT magnitude CSV."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="export_fft_spectrum",
    title="Export Fft Spectrum",
    summary="Write an FFT magnitude CSV.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
