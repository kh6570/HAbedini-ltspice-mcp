# In the name of God, the Most Gracious, the Most Merciful
"""Rename InstName."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="rename_component_reference",
    title="Rename Component Reference",
    summary="Rename InstName.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
