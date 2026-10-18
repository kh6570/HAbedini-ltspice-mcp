# In the name of God, the Most Gracious, the Most Merciful
"""Describe the GUI launch support."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="describe_live_gui_support",
    title="Describe Live Gui Support",
    summary="Describe the GUI launch support.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
