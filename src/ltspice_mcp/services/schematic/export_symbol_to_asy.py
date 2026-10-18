# In the name of God, the Most Gracious, the Most Merciful
"""Write a two-pin ``.asy`` named for a placed component."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="export_symbol_to_asy",
    title="Export Symbol To Asy",
    summary="Write a two-pin ``.asy`` named for a placed component.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
