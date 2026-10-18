# In the name of God, the Most Gracious, the Most Merciful
"""Add a ``.model`` directive."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_model",
    title="Add Model",
    summary="Add a ``.model`` directive.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
