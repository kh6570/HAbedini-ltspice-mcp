# In the name of God, the Most Gracious, the Most Merciful
"""Write a two-pin ``.asy`` symbol."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="create_asy_symbol",
    title="Create Asy Symbol",
    summary="Write a two-pin ``.asy`` symbol.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
