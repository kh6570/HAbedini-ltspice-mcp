# In the name of God, the Most Gracious, the Most Merciful
"""Prepare two corners and run them."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="run_worst_case",
    title="Run Worst Case",
    summary="Prepare two corners and run them.",
    phase="implemented",
    read_only=False,
    long_running=True,
    destructive=False,
    idempotent=False,
)
