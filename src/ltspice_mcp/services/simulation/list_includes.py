# In the name of God, the Most Gracious, the Most Merciful
"""List ``.lib`` and ``.include`` directives."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_includes",
    title="List Includes",
    summary="List ``.lib`` and ``.include`` directives.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
