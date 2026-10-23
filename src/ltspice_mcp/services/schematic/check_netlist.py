# In the name of God, the Most Gracious, the Most Merciful
"""Report structural problems in a netlist."""

from __future__ import annotations

from ltspice_mcp.services._backends.schematic_checks import CHECK_OUTPUT_SCHEMA
from ltspice_mcp.services.schematic.operations import check_netlist
from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="check_netlist",
    title="Check Netlist",
    summary="Report structural problems in a .net or .cir file.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
    output_schema=CHECK_OUTPUT_SCHEMA,
)

__all__ = ["SERVICE_SPEC", "check_netlist"]
