# In the name of God, the Most Gracious, the Most Merciful
"""Insert a ``.net`` network-parameter directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_net",
    title="Prepare Net",
    summary="Insert a ``.net`` network-parameter directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
