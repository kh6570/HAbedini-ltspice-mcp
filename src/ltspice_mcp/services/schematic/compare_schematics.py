# In the name of God, the Most Gracious, the Most Merciful
"""Compare component values between two schematics."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="compare_schematics",
    title="Compare Schematics",
    summary="Compare component values between two schematics.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
