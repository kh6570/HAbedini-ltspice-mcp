# In the name of God, the Most Gracious, the Most Merciful
"""Set a component model."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="set_element_model",
    title="Set Element Model",
    summary="Set a component model.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
