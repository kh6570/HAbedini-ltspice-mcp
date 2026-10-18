# In the name of God, the Most Gracious, the Most Merciful
"""Report that GUI events are unsupported."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="poll_live_gui_session_events",
    title="Poll Live Gui Session Events",
    summary="Report that GUI events are unsupported.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
