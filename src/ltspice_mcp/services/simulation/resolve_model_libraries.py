# In the name of God, the Most Gracious, the Most Merciful
"""Search the workspace and the LTspice lib tree for a model name."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="resolve_model_libraries",
    title="Resolve Model Libraries",
    summary="Search the workspace and the LTspice lib tree for a model name.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
