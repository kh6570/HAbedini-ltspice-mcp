# In the name of God, the Most Gracious, the Most Merciful
"""Check that a contribution JSON object has the required keys."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="validate_topology_contribution",
    title="Validate Topology Contribution",
    summary="Check that a contribution JSON object has the required keys.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
