# In the name of God, the Most Gracious, the Most Merciful
"""Insert a ``.meas`` directive without replacing other measurements."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_meas",
    title="Prepare Meas",
    summary="Insert a ``.meas`` directive without replacing other measurements.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
