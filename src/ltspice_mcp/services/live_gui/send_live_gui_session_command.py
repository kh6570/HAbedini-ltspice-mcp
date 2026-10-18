# In the name of God, the Most Gracious, the Most Merciful
"""Report that GUI commands are unsupported."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="send_live_gui_session_command",
    title="Send Live Gui Session Command",
    summary="Report that GUI commands are unsupported.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
