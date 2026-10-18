# In the name of God, the Most Gracious, the Most Merciful
"""List topology notes."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_topology_blocks",
    title="List Topology Blocks",
    summary="List topology notes.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
