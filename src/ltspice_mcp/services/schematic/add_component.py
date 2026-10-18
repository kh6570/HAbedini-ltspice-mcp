# In the name of God, the Most Gracious, the Most Merciful
"""Place a primitive component."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_component",
    title="Add Component",
    summary="Place a primitive component.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
