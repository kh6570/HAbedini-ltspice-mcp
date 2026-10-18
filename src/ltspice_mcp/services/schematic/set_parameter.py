# In the name of God, the Most Gracious, the Most Merciful
"""Add or replace a ``.param`` directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="set_parameter",
    title="Set Parameter",
    summary="Add or replace a ``.param`` directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
