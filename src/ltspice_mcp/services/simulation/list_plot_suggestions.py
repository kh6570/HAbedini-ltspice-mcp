# In the name of God, the Most Gracious, the Most Merciful
"""Suggest voltages and currents an agent can plot."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="list_plot_suggestions",
    title="List Plot Suggestions",
    summary="Suggest voltages and currents an agent can plot.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
