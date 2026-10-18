# In the name of God, the Most Gracious, the Most Merciful
"""State what mixed-signal authoring LTspice can and cannot do."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_mixed_signal_support",
    title="Describe Mixed Signal Support",
    summary="State what mixed-signal authoring LTspice can and cannot do.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
