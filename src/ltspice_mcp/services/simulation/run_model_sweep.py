# In the name of God, the Most Gracious, the Most Merciful
"""Run once per model name."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="run_model_sweep",
    title="Run Model Sweep",
    summary="Run once per model name.",
    phase="implemented",
    read_only=False,
    long_running=True,
    destructive=False,
    idempotent=False,
)
