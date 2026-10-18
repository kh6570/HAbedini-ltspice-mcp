# In the name of God, the Most Gracious, the Most Merciful
"""Write one signal as whitespace-separated text."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="export_waveform_ascii",
    title="Export Waveform Ascii",
    summary="Write one signal as whitespace-separated text.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
