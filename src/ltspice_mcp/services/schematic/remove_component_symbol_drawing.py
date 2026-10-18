# In the name of God, the Most Gracious, the Most Merciful
"""Remove one symbol drawing by index."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="remove_component_symbol_drawing",
    title="Remove Component Symbol Drawing",
    summary="Remove one symbol drawing by index.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=True,
    idempotent=False,
)
