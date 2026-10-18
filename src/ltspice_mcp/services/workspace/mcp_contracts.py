# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "write_workspace_text_file": {
        "title": "Write Workspace Text File",
        "description": "Write a text file inside the workspace.",
        "input_schema": {
            "type": "object",
            "properties": {"relative_path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["relative_path", "content"],
        },
    }
}
