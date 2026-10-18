# In the name of God, the Most Gracious, the Most Merciful
"""Append a LINE, RECTANGLE, CIRCLE, or ARC to a symbol."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_component_symbol_drawing",
    title="Add Component Symbol Drawing",
    summary="Append a LINE, RECTANGLE, CIRCLE, or ARC to a symbol.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
