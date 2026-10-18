# In the name of God, the Most Gracious, the Most Merciful
"""Describe one reference circuit."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_reference_circuit_recipe",
    title="Describe Reference Circuit Recipe",
    summary="Describe one reference circuit.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
