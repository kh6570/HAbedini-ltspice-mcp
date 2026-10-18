# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "list_workflow_instructions": {
        "title": "List Workflow Instructions",
        "description": "List bundled workflow notes.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "read_workflow_instruction": {
        "title": "Read Workflow Instruction",
        "description": "Read one bundled workflow note.",
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    },
}
