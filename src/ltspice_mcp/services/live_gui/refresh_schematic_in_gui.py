# In the name of God, the Most Gracious, the Most Merciful
"""Close and reopen the schematic so the GUI reloads the file."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="refresh_schematic_in_gui",
    title="Refresh Schematic In Gui",
    summary="Close and reopen the schematic so the GUI reloads the file.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
