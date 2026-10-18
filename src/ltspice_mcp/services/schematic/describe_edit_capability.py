# In the name of God, the Most Gracious, the Most Merciful
"""Describe which edits the clean-room editor performs."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_edit_capability",
    title="Describe Edit Capability",
    summary="Describe which edits the clean-room editor performs.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
