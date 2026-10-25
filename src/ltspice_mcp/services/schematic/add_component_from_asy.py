# In the name of God, the Most Gracious, the Most Merciful
"""Place a symbol. Use the file name of an ``.asy`` in the workspace."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="add_component_from_asy",
    title="Add Component From Asy",
    summary="Place a symbol using the file name of an ``.asy`` in the workspace.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
