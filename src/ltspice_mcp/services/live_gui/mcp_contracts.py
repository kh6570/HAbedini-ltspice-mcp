# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "close_live_gui_session": {
        "title": "Close Live Gui Session",
        "description": "Stop a GUI process this server launched.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "describe_live_gui_support": {
        "title": "Describe Live Gui Support",
        "description": "Describe the GUI launch support.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "open_schematic_in_gui": {
        "title": "Open Schematic In Gui",
        "description": "Launch LTspice on a schematic without ``-b``.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "poll_live_gui_session": {
        "title": "Poll Live Gui Session",
        "description": "Report that polling a GUI session is unsupported.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "poll_live_gui_session_events": {
        "title": "Poll Live Gui Session Events",
        "description": "Report that GUI events are unsupported.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "refresh_schematic_in_gui": {
        "title": "Refresh Schematic In Gui",
        "description": "Close and reopen the schematic so the GUI reloads the file.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "send_live_gui_session_command": {
        "title": "Send Live Gui Session Command",
        "description": "Report that GUI commands are unsupported.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "command": {"type": "string"}},
            "required": ["schematic_path", "command"],
        },
    },
}
