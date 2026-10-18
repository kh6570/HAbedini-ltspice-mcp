# In the name of God, the Most Gracious, the Most Merciful
"""Step-response scalars."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="measure_step_response",
    title="Measure Step Response",
    summary="Step-response scalars.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
