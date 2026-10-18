# In the name of God, the Most Gracious, the Most Merciful
"""Write ``.meas`` rows to CSV."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="export_measures_csv",
    title="Export Measures Csv",
    summary="Write ``.meas`` rows to CSV.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
