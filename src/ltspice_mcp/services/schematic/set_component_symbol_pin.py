# In the name of God, the Most Gracious, the Most Merciful
"""Move or add a symbol pin."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="set_component_symbol_pin",
    title="Set Component Symbol Pin",
    summary="Move or add a symbol pin.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
