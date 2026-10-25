# In the name of God, the Most Gracious, the Most Merciful
"""Summarize the raw files in a batch directory."""

from __future__ import annotations

from ltspice_mcp.services.service_spec import ServiceSpec

SERVICE_SPEC = ServiceSpec(
    name="summarize_batch",
    title="Summarize Batch",
    summary="Summarize raw files sitting in a batch directory.",
    phase="implemented",
    read_only=True,
    long_running=False,
    destructive=False,
    idempotent=True,
)
