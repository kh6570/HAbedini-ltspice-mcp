# In the name of God, the Most Gracious, the Most Merciful
"""Set one ``.asy`` attribute."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="set_component_symbol_text",
    title="Set Component Symbol Text",
    summary="Set one ``.asy`` attribute.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
