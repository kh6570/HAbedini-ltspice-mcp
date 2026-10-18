# In the name of God, the Most Gracious, the Most Merciful
"""Count operating-point rows by unit."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="summarize_device_operating_points",
    title="Summarize Device Operating Points",
    summary="Count operating-point rows by unit.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
