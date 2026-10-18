# In the name of God, the Most Gracious, the Most Merciful
"""Search titles and summaries."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="search_topology_blocks",
    title="Search Topology Blocks",
    summary="Search titles and summaries.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
