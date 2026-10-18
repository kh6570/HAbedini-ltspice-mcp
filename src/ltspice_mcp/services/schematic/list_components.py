# In the name of God, the Most Gracious, the Most Merciful
"""List placed components."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_components",
    title="List Components",
    summary="List placed components.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
