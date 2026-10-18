# In the name of God, the Most Gracious, the Most Merciful
"""Average output power over average input power."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="measure_efficiency",
    title="Measure Efficiency",
    summary="Average output power over average input power.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
