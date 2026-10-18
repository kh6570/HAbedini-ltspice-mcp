# In the name of God, the Most Gracious, the Most Merciful
"""Place a library symbol by name."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_library_component",
    title="Add Library Component",
    summary="Place a library symbol by name.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
