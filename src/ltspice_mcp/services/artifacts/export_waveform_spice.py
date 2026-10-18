# In the name of God, the Most Gracious, the Most Merciful
"""Write a PWL statement for one real trace."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="export_waveform_spice",
    title="Export Waveform Spice",
    summary="Write a PWL statement for one real trace.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
