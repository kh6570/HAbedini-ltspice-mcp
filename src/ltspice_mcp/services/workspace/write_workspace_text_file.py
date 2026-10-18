# In the name of God, the Most Gracious, the Most Merciful
"""Write a text file inside the workspace."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="write_workspace_text_file",
    title="Write Workspace Text File",
    summary="Write a text file inside the workspace.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
