# In the name of God, the Most Gracious, the Most Merciful
"""Insert a ``.options`` directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_options",
    title="Prepare Options",
    summary="Insert a ``.options`` directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
