# In the name of God, the Most Gracious, the Most Merciful
"""Insert a ``.param`` directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_param",
    title="Prepare Param",
    summary="Insert a ``.param`` directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
