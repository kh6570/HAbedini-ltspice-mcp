# In the name of God, the Most Gracious, the Most Merciful
"""Return artifact paths recorded for a finished session."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="download_remote_artifacts",
    title="Download Remote Artifacts",
    summary="Return artifact paths recorded for a finished session.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
