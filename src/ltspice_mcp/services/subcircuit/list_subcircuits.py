# In the name of God, the Most Gracious, the Most Merciful
"""List ``.subckt`` blocks and hierarchical symbols."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_subcircuits",
    title="List Subcircuits",
    summary="List ``.subckt`` blocks and hierarchical symbols.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
