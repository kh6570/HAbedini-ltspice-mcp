# In the name of God, the Most Gracious, the Most Merciful
"""Run one batch simulation."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="run_simulation",
    title="Run Simulation",
    summary="Run one batch simulation.",
    phase="implemented",
    read_only=False,
    long_running=True,
    destructive=False,
    idempotent=False,
)
