# In the name of God, the Most Gracious, the Most Merciful
"""Store a validated contribution under the workspace."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="ingest_topology_contribution",
    title="Ingest Topology Contribution",
    summary="Store a validated contribution under the workspace.",
    phase="implemented",
    read_only=False,
    long_running=False,
    destructive=False,
    idempotent=False,
)
