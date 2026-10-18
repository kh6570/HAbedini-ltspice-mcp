# In the name of God, the Most Gracious, the Most Merciful
"""Write a netlist with LTspice ``-netlist``, or the clean-room renderer."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="generate_netlist",
    title="Generate Netlist",
    summary="Write a netlist with LTspice ``-netlist``, or the clean-room renderer.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
