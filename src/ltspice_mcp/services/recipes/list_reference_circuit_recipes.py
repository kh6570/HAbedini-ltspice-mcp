# In the name of God, the Most Gracious, the Most Merciful
"""List bundled reference circuits."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_reference_circuit_recipes",
    title="List Reference Circuit Recipes",
    summary="List bundled reference circuits.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
