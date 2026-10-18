# In the name of God, the Most Gracious, the Most Merciful
"""Report that polling a GUI session is unsupported."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="poll_live_gui_session",
    title="Poll Live Gui Session",
    summary="Report that polling a GUI session is unsupported.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
