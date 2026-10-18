# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "list_subcircuits": {
        "title": "List Subcircuits",
        "description": "List ``.subckt`` blocks and hierarchical symbols.",
        "input_schema": {
            "type": "object",
            "properties": {"source_path": {"type": "string"}},
            "required": ["source_path"],
        },
    },
    "read_subcircuit": {
        "title": "Read Subcircuit",
        "description": "Return one ``.subckt`` body or a hierarchical sheet.",
        "input_schema": {
            "type": "object",
            "properties": {"source_path": {"type": "string"}, "name": {"type": "string"}},
            "required": ["source_path", "name"],
        },
    },
    "set_subcircuit_component_parameters": {
        "title": "Set Subcircuit Component Parameters",
        "description": "Set SpiceLine on a component inside a schematic subcircuit file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "spice_line": {"type": "string"},
                "spice_line2": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "spice_line"],
        },
    },
    "set_subcircuit_component_value": {
        "title": "Set Subcircuit Component Value",
        "description": "Set a value on a component inside a schematic subcircuit file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "value"],
        },
    },
}
