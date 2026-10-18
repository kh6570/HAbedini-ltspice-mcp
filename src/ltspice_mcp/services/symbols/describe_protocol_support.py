# In the name of God, the Most Gracious, the Most Merciful
"""State that I2C and SPI scaffolds here are behavioral teaching circuits."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_protocol_support",
    title="Describe Protocol Support",
    summary="State that I2C and SPI scaffolds here are behavioral teaching circuits.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
