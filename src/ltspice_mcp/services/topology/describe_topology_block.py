# In the name of God, the Most Gracious, the Most Merciful
"""Return one topology note."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_topology_block",
    title="Describe Topology Block",
    summary="Return one topology note.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
