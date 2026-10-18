# In the name of God, the Most Gracious, the Most Merciful
"""Launch LTspice on a schematic without ``-b``."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="open_schematic_in_gui",
    title="Open Schematic In Gui",
    summary="Launch LTspice on a schematic without ``-b``.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
