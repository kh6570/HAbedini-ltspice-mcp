# In the name of God, the Most Gracious, the Most Merciful
"""Insert a ``.func`` directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_func",
    title="Prepare Func",
    summary="Insert a ``.func`` directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
