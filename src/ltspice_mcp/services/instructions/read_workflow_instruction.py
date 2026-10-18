# In the name of God, the Most Gracious, the Most Merciful
"""Read one bundled workflow note."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="read_workflow_instruction",
    title="Read Workflow Instruction",
    summary="Read one bundled workflow note.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
