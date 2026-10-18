# In the name of God, the Most Gracious, the Most Merciful
"""Write a behavioral sketch of a SPI data latch, not a protocol engine."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="scaffold_spi_device",
    title="Scaffold Spi Device",
    summary="Write a behavioral sketch of a SPI data latch, not a protocol engine.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
