# In the name of God, the Most Gracious, the Most Merciful
"""Read ``.meas`` results."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="read_measures",
    title="Read Measures",
    summary="Read ``.meas`` results.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
