# In the name of God, the Most Gracious, the Most Merciful
"""Insert a ``.nodeset`` directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="prepare_nodeset",
    title="Prepare Nodeset",
    summary="Insert a ``.nodeset`` directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
