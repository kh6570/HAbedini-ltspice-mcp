# In the name of God, the Most Gracious, the Most Merciful
"""Insert a ``.four`` directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_four",
    title="Prepare Four",
    summary="Insert a ``.four`` directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
