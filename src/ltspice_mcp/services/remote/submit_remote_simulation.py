# In the name of God, the Most Gracious, the Most Merciful
"""Start a background local simulation and return a session id."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="submit_remote_simulation",
    title="Submit Remote Simulation",
    summary="Start a background local simulation and return a session id.",
    phase="implemented",
    read_only=False,
    long_running=True,
    destructive=False,
    idempotent=False,
)
