# In the name of God, the Most Gracious, the Most Merciful
"""Insert a ``.tf`` directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_transfer_function",
    title="Prepare Transfer Function",
    summary="Insert a ``.tf`` directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
