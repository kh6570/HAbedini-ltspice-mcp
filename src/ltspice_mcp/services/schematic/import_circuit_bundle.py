# In the name of God, the Most Gracious, the Most Merciful
"""Unpack a zip of schematics into the workspace, or copy one ``.asc``."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="import_circuit_bundle",
    title="Import Circuit Bundle",
    summary="Unpack a zip of schematics into the workspace, or copy one ``.asc``.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
