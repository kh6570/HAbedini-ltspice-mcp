# In the name of God, the Most Gracious, the Most Merciful
"""List ``.meas`` names."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_measures",
    title="List Measures",
    summary="List ``.meas`` names.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
