# In the name of God, the Most Gracious, the Most Merciful
"""Return the status of a background session."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="poll_remote_run",
    title="Poll Remote Run",
    summary="Return the status of a background session.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
