# In the name of God, the Most Gracious, the Most Merciful
"""Summarize a simulation log."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="read_log",
    title="Read Log",
    summary="Summarize a simulation log.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
