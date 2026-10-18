# In the name of God, the Most Gracious, the Most Merciful
"""Summarize a schematic."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="inspect_schematic",
    title="Inspect Schematic",
    summary="Summarize a schematic.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
