# In the name of God, the Most Gracious, the Most Merciful
"""Explain that LTspice junctions are implicit."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="remove_junction",
    title="Remove Junction",
    summary="Explain that LTspice junctions are implicit.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=True,
    idempotent=False,
)
