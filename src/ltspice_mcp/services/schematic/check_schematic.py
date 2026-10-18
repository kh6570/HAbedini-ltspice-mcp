# In the name of God, the Most Gracious, the Most Merciful
"""Report structural problems without running LTspice."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="check_schematic",
    title="Check Schematic",
    summary="Report structural problems without running LTspice.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
