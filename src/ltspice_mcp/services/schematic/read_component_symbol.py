# In the name of God, the Most Gracious, the Most Merciful
"""Read an ``.asy`` symbol."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="read_component_symbol",
    title="Read Component Symbol",
    summary="Read an ``.asy`` symbol.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
