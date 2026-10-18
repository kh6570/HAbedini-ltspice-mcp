# In the name of God, the Most Gracious, the Most Merciful
"""Run the schematic once per component value."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="run_value_sweep",
    title="Run Value Sweep",
    summary="Run the schematic once per component value.",
    phase="implemented",
    read_only=False,
    long_running=True,
    destructive=False,
    idempotent=False,
)
