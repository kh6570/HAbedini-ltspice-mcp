# In the name of God, the Most Gracious, the Most Merciful
"""Draw a simple schematic preview."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="render_schematic_image",
    title="Render Schematic Image",
    summary="Draw a simple schematic preview.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
