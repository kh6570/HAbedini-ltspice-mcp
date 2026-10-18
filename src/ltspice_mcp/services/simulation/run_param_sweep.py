# In the name of God, the Most Gracious, the Most Merciful
"""Add a ``.step`` and run once. LTspice expands the steps."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="run_param_sweep",
    title="Run Param Sweep",
    summary="Add a ``.step`` and run once. LTspice expands the steps.",
    phase="implemented",
    read_only=False,
    long_running=True,
    destructive=False,
    idempotent=False,
)
