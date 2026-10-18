# In the name of God, the Most Gracious, the Most Merciful
"""Step a component between two corner values with ``table()``."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_worst_case",
    title="Prepare Worst Case",
    summary="Step a component between two corner values with ``table()``.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
