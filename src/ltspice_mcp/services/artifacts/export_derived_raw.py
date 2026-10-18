# In the name of God, the Most Gracious, the Most Merciful
"""Write a small ASCII raw file containing one trace."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="export_derived_raw",
    title="Export Derived Raw",
    summary="Write a small ASCII raw file containing one trace.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
