# In the name of God, the Most Gracious, the Most Merciful
"""Write selected signals to CSV."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="export_waveform_csv",
    title="Export Waveform Csv",
    summary="Write selected signals to CSV.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
