# In the name of God, the Most Gracious, the Most Merciful
"""List stepped runs from a raw file and, when given, the log."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_steps",
    title="List Steps",
    summary="List stepped runs from a raw file and, when given, the log.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
