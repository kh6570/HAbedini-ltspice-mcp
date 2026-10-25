# In the name of God, the Most Gracious, the Most Merciful
"""Remove a directive or a comment that contains ``text``."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="remove_instruction",
    title="Remove Instruction",
    summary="Remove a directive or comment containing ``text``.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=True,
    idempotent=False,
)
