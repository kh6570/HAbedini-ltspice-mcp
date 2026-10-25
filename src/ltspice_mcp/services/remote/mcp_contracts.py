# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "close_remote_session": {
        "title": "Close Remote Session",
        "description": "Drop a session from memory. The files stay in place on the disk.",
        "input_schema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    "download_remote_artifacts": {
        "title": "Download Remote Artifacts",
        "description": "Return artifact paths recorded for a finished session.",
        "input_schema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    "poll_remote_run": {
        "title": "Poll Remote Run",
        "description": "Return the status of a background session.",
        "input_schema": {
            "type": "object",
            "properties": {"session_id": {"type": "string"}},
            "required": ["session_id"],
        },
    },
    "submit_remote_simulation": {
        "title": "Submit Remote Simulation",
        "description": "Start a background local simulation and return a session id.",
        "input_schema": {
            "type": "object",
            "properties": {"source_path": {"type": "string"}},
            "required": ["source_path"],
        },
    },
}
