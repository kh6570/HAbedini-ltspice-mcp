# In the name of God, the Most Gracious, the Most Merciful
"""Drop a session from memory. Files on disk are left in place."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="close_remote_session",
    title="Close Remote Session",
    summary="Drop a session from memory. Files on disk are left in place.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
