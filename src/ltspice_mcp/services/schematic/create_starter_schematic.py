# In the name of God, the Most Gracious, the Most Merciful
"""Create a divider, RC, or buck starter schematic."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="create_starter_schematic",
    title="Create Starter Schematic",
    summary="Create a divider, RC, or buck starter schematic.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
