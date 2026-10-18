# In the name of God, the Most Gracious, the Most Merciful
"""Prepare a Monte Carlo ``.step`` and run it."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="run_monte_carlo",
    title="Run Monte Carlo",
    summary="Prepare a Monte Carlo ``.step`` and run it.",
    phase="implemented",
    read_only=False,
    long_running=True,
    destructive=False,
    idempotent=False,
)
