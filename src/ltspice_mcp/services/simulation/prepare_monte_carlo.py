# In the name of God, the Most Gracious, the Most Merciful
"""Point a component at ``mc()`` and step the run index."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_monte_carlo",
    title="Prepare Monte Carlo",
    summary="Point a component at ``mc()`` and step the run index.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
