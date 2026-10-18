# In the name of God, the Most Gracious, the Most Merciful
"""Summarize min, max, and mean of a stepped trace."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="summarize_tolerance_analysis",
    title="Summarize Tolerance Analysis",
    summary="Summarize min, max, and mean of a stepped trace.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
