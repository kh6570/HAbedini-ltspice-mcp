# In the name of God, the Most Gracious, the Most Merciful
"""Report structural problems. Do not start LTspice."""

from __future__ import annotations

from ltspice_mcp.services._backends.schematic_checks import CHECK_OUTPUT_SCHEMA
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
    output_schema=CHECK_OUTPUT_SCHEMA,
)
