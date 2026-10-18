# In the name of God, the Most Gracious, the Most Merciful
"""Copy a schematic to a new path."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="save_schematic_as",
    title="Save Schematic As",
    summary="Copy a schematic to a new path.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
