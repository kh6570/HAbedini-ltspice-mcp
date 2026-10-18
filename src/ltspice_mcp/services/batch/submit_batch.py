# In the name of God, the Most Gracious, the Most Merciful
"""Run one schematic and keep a manifest of the artifacts."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="submit_batch",
    title="Submit Batch",
    summary="Run one schematic and keep a manifest of the artifacts.",
    phase="implemented",
    read_only=False,
    long_running=True,
    destructive=False,
    idempotent=False,
)
