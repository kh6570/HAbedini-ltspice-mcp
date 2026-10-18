# In the name of God, the Most Gracious, the Most Merciful
"""Write a recipe schematic into the workspace."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="materialize_recipe",
    title="Materialize Recipe",
    summary="Write a recipe schematic into the workspace.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
