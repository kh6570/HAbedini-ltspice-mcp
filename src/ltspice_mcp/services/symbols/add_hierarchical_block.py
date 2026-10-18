# In the name of God, the Most Gracious, the Most Merciful
"""Create a child sheet with In/Out pins and place it on the parent."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_hierarchical_block",
    title="Add Hierarchical Block",
    summary="Create a child sheet with In/Out pins and place it on the parent.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
