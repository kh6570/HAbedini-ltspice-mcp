# In the name of God, the Most Gracious, the Most Merciful
"""Reset attribute windows to left-justified text."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="normalize_component_text_rotation",
    title="Normalize Component Text Rotation",
    summary="Reset attribute windows to left-justified text.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
