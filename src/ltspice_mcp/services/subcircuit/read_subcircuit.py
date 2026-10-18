# In the name of God, the Most Gracious, the Most Merciful
"""Return one ``.subckt`` body or a hierarchical sheet."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="read_subcircuit",
    title="Read Subcircuit",
    summary="Return one ``.subckt`` body or a hierarchical sheet.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
