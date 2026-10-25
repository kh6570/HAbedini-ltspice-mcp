# In the name of God, the Most Gracious, the Most Merciful
"""Stage an AC loop-gain run. Use the extra-source method."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_loop_gain_analysis",
    title="Prepare Loop Gain Analysis",
    summary="Stage an AC loop-gain run using the extra-source method.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
