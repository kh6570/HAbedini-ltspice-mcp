# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "cancel_batch": {
        "title": "Cancel Batch",
        "description": "Mark a batch cancelled. A finished batch stays completed.",
        "input_schema": {
            "type": "object",
            "properties": {"batch_id": {"type": "string"}},
            "required": ["batch_id"],
        },
    },
    "collect_batch_results": {
        "title": "Collect Batch Results",
        "description": "Return the stored batch result.",
        "input_schema": {
            "type": "object",
            "properties": {"batch_id": {"type": "string"}},
            "required": ["batch_id"],
        },
    },
    "get_batch_status": {
        "title": "Get Batch Status",
        "description": "Return a batch manifest summary.",
        "input_schema": {
            "type": "object",
            "properties": {"batch_id": {"type": "string"}},
            "required": ["batch_id"],
        },
    },
    "submit_batch": {
        "title": "Submit Batch",
        "description": "Run one schematic and keep a manifest of the artifacts.",
        "input_schema": {
            "type": "object",
            "properties": {"source_path": {"type": "string"}},
            "required": ["source_path"],
        },
    },
}
