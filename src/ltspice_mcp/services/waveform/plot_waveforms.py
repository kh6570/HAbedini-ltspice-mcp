# In the name of God, the Most Gracious, the Most Merciful
"""Plot one or more comma-separated signals to a PNG."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="plot_waveforms",
    title="Plot Waveforms",
    summary="Plot one or more comma-separated signals to a PNG.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
