# In the name of God, the Most Gracious, the Most Merciful
"""Describe schematic edit support for clients."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_schematic_edit_support",
    title="Describe Schematic Edit Support",
    summary="Describe schematic edit support for clients.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
