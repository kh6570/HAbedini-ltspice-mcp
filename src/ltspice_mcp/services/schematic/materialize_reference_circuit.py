# In the name of God, the Most Gracious, the Most Merciful
"""Write a built-in reference circuit."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="materialize_reference_circuit",
    title="Materialize Reference Circuit",
    summary="Write a built-in reference circuit.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
