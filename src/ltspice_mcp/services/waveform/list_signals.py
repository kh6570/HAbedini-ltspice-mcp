# In the name of God, the Most Gracious, the Most Merciful
"""List signals in a raw file."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_signals",
    title="List Signals",
    summary="List signals in a raw file.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
