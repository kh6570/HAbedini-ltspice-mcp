# In the name of God, the Most Gracious, the Most Merciful
"""Remove a component."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="remove_component",
    title="Remove Component",
    summary="Remove a component.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=True,
    idempotent=False,
)
