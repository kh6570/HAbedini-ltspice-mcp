# In the name of God, the Most Gracious, the Most Merciful
"""Copy a netlist inside the workspace."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="save_netlist_copy",
    title="Save Netlist Copy",
    summary="Copy a netlist inside the workspace.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
