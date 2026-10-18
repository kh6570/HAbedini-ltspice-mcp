# In the name of God, the Most Gracious, the Most Merciful
"""List bundled workflow notes."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_workflow_instructions",
    title="List Workflow Instructions",
    summary="List bundled workflow notes.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
