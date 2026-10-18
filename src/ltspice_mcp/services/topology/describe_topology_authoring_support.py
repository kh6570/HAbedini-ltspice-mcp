# In the name of God, the Most Gracious, the Most Merciful
"""Describe the topology note format."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_topology_authoring_support",
    title="Describe Topology Authoring Support",
    summary="Describe the topology note format.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
