# In the name of God, the Most Gracious, the Most Merciful
"""Describe a built-in layout spec."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_schematic_layout_spec",
    title="Describe Schematic Layout Spec",
    summary="Describe a built-in layout spec.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
