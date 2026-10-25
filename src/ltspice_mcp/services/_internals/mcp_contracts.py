# In the name of God, the Most Gracious, the Most Merciful
"""These contracts describe tools that a service package does not discover."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "describe_server_capabilities": {
        "title": "Describe Server Capabilities",
        "description": "Report the LTspice engine, tool groups, and feature flags.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }
}
