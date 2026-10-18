# In the name of God, the Most Gracious, the Most Merciful
"""Stop a GUI process this server launched."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="close_live_gui_session",
    title="Close Live Gui Session",
    summary="Stop a GUI process this server launched.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
