# In the name of God, the Most Gracious, the Most Merciful
"""Stop a simulation started for this source path."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="cancel_run",
    title="Cancel Run",
    summary="Stop a simulation started for this source path.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=True,
    idempotent=False,
)
