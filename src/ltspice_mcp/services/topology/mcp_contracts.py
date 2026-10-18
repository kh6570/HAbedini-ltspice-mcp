# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "describe_topology_authoring_support": {
        "title": "Describe Topology Authoring Support",
        "description": "Describe the topology note format.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "describe_topology_block": {
        "title": "Describe Topology Block",
        "description": "Return one topology note.",
        "input_schema": {
            "type": "object",
            "properties": {"block_id": {"type": "string"}},
            "required": ["block_id"],
        },
    },
    "ingest_topology_contribution": {
        "title": "Ingest Topology Contribution",
        "description": "Store a validated contribution under the workspace.",
        "input_schema": {
            "type": "object",
            "properties": {"payload": {"type": "string"}},
            "required": ["payload"],
        },
    },
    "list_topology_blocks": {
        "title": "List Topology Blocks",
        "description": "List topology notes.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "search_topology_blocks": {
        "title": "Search Topology Blocks",
        "description": "Search titles and summaries.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    "validate_topology_contribution": {
        "title": "Validate Topology Contribution",
        "description": "Check that a contribution JSON object has the required keys.",
        "input_schema": {
            "type": "object",
            "properties": {"payload": {"type": "string"}},
            "required": ["payload"],
        },
    },
}
