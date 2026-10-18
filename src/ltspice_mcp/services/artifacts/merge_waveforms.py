# In the name of God, the Most Gracious, the Most Merciful
"""Return two traces side by side without writing a combined raw file."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="merge_waveforms",
    title="Merge Waveforms",
    summary="Return two traces side by side without writing a combined raw file.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
