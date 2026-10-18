# In the name of God, the Most Gracious, the Most Merciful
"""Create an empty schematic."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="create_schematic",
    title="Create Schematic",
    summary="Create an empty schematic.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
