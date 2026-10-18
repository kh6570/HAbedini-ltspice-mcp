# In the name of God, the Most Gracious, the Most Merciful
"""Replace a schematic with a built-in layout."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="apply_schematic_layout_spec",
    title="Apply Schematic Layout Spec",
    summary="Replace a schematic with a built-in layout.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
