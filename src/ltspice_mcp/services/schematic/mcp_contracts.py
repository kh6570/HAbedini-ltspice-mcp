# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "add_component": {
        "title": "Add Component",
        "description": "Place a primitive component.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "kind": {"type": "string"},
                "reference": {"type": "string"},
                "value": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "rotation": {"type": "string"},
            },
            "required": ["schematic_path", "kind", "reference"],
        },
    },
    "add_component_from_asy": {
        "title": "Add Component From Asy",
        "description": "Place a symbol using the file name of an ``.asy`` in the workspace.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "asy_path": {"type": "string"},
                "reference": {"type": "string"},
                "value": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "rotation": {"type": "string"},
            },
            "required": ["schematic_path", "asy_path", "reference"],
        },
    },
    "add_component_symbol_drawing": {
        "title": "Add Component Symbol Drawing",
        "description": "Append a LINE, RECTANGLE, CIRCLE, or ARC to a symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "asy_path": {"type": "string"},
                "kind": {"type": "string"},
                "coords": {"type": "string"},
            },
            "required": ["asy_path", "kind", "coords"],
        },
    },
    "add_instruction": {
        "title": "Add Instruction",
        "description": "Add a SPICE directive or a comment.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "text": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
            },
            "required": ["schematic_path", "text"],
        },
    },
    "add_junction": {
        "title": "Add Junction",
        "description": "Split a wire so a coordinate becomes a junction.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
            },
            "required": ["schematic_path", "x", "y"],
        },
    },
    "add_library_component": {
        "title": "Add Library Component",
        "description": "Place a library symbol by name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "symbol_name": {"type": "string"},
                "reference": {"type": "string"},
                "value": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "rotation": {"type": "string"},
            },
            "required": ["schematic_path", "symbol_name", "reference"],
        },
    },
    "add_net_label": {
        "title": "Add Net Label",
        "description": "Add a net label.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "name": {"type": "string"},
            },
            "required": ["schematic_path", "x", "y", "name"],
        },
    },
    "add_wire": {
        "title": "Add Wire",
        "description": "Add a wire. Exposed as ``add_wire`` by the tool module.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "x1": {"type": "integer"},
                "y1": {"type": "integer"},
                "x2": {"type": "integer"},
                "y2": {"type": "integer"},
            },
            "required": ["schematic_path", "x1", "y1", "x2", "y2"],
        },
    },
    "apply_schematic_layout_spec": {
        "title": "Apply Schematic Layout Spec",
        "description": "Replace a schematic with a built-in layout.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "spec_name": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "check_schematic": {
        "title": "Check Schematic",
        "description": "Report structural problems without running LTspice.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "compare_schematics": {
        "title": "Compare Schematics",
        "description": "Compare component values between two schematics.",
        "input_schema": {
            "type": "object",
            "properties": {"left_path": {"type": "string"}, "right_path": {"type": "string"}},
            "required": ["left_path", "right_path"],
        },
    },
    "create_schematic": {
        "title": "Create Schematic",
        "description": "Create an empty schematic.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "create_starter_schematic": {
        "title": "Create Starter Schematic",
        "description": "Create a divider, RC, or buck starter schematic.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "kind": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "describe_edit_capability": {
        "title": "Describe Edit Capability",
        "description": "Describe which edits the clean-room editor performs.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "describe_schematic_edit_support": {
        "title": "Describe Schematic Edit Support",
        "description": "Describe schematic edit support for clients.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "describe_schematic_layout_spec": {
        "title": "Describe Schematic Layout Spec",
        "description": "Describe a built-in layout spec.",
        "input_schema": {
            "type": "object",
            "properties": {"spec_name": {"type": "string"}},
            "required": [],
        },
    },
    "export_symbol_to_asy": {
        "title": "Export Symbol To Asy",
        "description": "Write a two-pin ``.asy`` named for a placed component.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "output_path": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "output_path"],
        },
    },
    "import_circuit_bundle": {
        "title": "Import Circuit Bundle",
        "description": "Unpack a zip of schematics into the workspace, or copy one ``.asc``.",
        "input_schema": {
            "type": "object",
            "properties": {
                "bundle_path": {"type": "string"},
                "destination_dir": {"type": "string"},
            },
            "required": ["bundle_path"],
        },
    },
    "inspect_schematic": {
        "title": "Inspect Schematic",
        "description": "Summarize a schematic.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "list_components": {
        "title": "List Components",
        "description": "List placed components.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "materialize_reference_circuit": {
        "title": "Materialize Reference Circuit",
        "description": "Write a built-in reference circuit.",
        "input_schema": {
            "type": "object",
            "properties": {"recipe_id": {"type": "string"}, "destination_path": {"type": "string"}},
            "required": ["recipe_id", "destination_path"],
        },
    },
    "normalize_component_text_rotation": {
        "title": "Normalize Component Text Rotation",
        "description": "Reset attribute windows to left-justified text.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "read_component": {
        "title": "Read Component",
        "description": "Read one component.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "reference": {"type": "string"}},
            "required": ["schematic_path", "reference"],
        },
    },
    "read_component_symbol": {
        "title": "Read Component Symbol",
        "description": "Read an ``.asy`` symbol.",
        "input_schema": {
            "type": "object",
            "properties": {"symbol_path": {"type": "string"}},
            "required": ["symbol_path"],
        },
    },
    "read_net_connectivity": {
        "title": "Read Net Connectivity",
        "description": "Return primitive pin-to-net connectivity.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "remove_component": {
        "title": "Remove Component",
        "description": "Remove a component.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "reference": {"type": "string"}},
            "required": ["schematic_path", "reference"],
        },
    },
    "remove_component_symbol_drawing": {
        "title": "Remove Component Symbol Drawing",
        "description": "Remove one symbol drawing by index.",
        "input_schema": {
            "type": "object",
            "properties": {"asy_path": {"type": "string"}, "index": {"type": "integer"}},
            "required": ["asy_path", "index"],
        },
    },
    "remove_instruction": {
        "title": "Remove Instruction",
        "description": "Remove a directive or comment containing ``text``.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "text": {"type": "string"}},
            "required": ["schematic_path", "text"],
        },
    },
    "remove_junction": {
        "title": "Remove Junction",
        "description": "Explain that LTspice junctions are implicit.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
            },
            "required": ["schematic_path", "x", "y"],
        },
    },
    "remove_net_label": {
        "title": "Remove Net Label",
        "description": "Remove a net label.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "name": {"type": "string"},
            },
            "required": ["schematic_path", "x", "y"],
        },
    },
    "remove_wire": {
        "title": "Remove Wire",
        "description": "Remove a wire.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "x1": {"type": "integer"},
                "y1": {"type": "integer"},
                "x2": {"type": "integer"},
                "y2": {"type": "integer"},
            },
            "required": ["schematic_path", "x1", "y1", "x2", "y2"],
        },
    },
    "rename_component_reference": {
        "title": "Rename Component Reference",
        "description": "Rename InstName.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "new_reference": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "new_reference"],
        },
    },
    "render_schematic_image": {
        "title": "Render Schematic Image",
        "description": "Draw a simple schematic preview.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "output_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "save_schematic_as": {
        "title": "Save Schematic As",
        "description": "Copy a schematic to a new path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "destination_path": {"type": "string"},
            },
            "required": ["schematic_path", "destination_path"],
        },
    },
    "set_component_parameters": {
        "title": "Set Component Parameters",
        "description": "Set SpiceLine attributes.",
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
    "set_component_position": {
        "title": "Set Component Position",
        "description": "Move a component and wires that ended on its pins.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "rotation": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "x", "y"],
        },
    },
    "set_component_symbol_pin": {
        "title": "Set Component Symbol Pin",
        "description": "Move or add a symbol pin.",
        "input_schema": {
            "type": "object",
            "properties": {
                "asy_path": {"type": "string"},
                "pin_name": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "spice_order": {"type": "integer"},
            },
            "required": ["asy_path", "pin_name", "x", "y", "spice_order"],
        },
    },
    "set_component_symbol_text": {
        "title": "Set Component Symbol Text",
        "description": "Set one ``.asy`` attribute.",
        "input_schema": {
            "type": "object",
            "properties": {
                "asy_path": {"type": "string"},
                "attribute": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["asy_path", "attribute", "value"],
        },
    },
    "set_component_value": {
        "title": "Set Component Value",
        "description": "Set a component value.",
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
    "set_element_model": {
        "title": "Set Element Model",
        "description": "Set a component model.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "model": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "model"],
        },
    },
    "set_parameter": {
        "title": "Set Parameter",
        "description": "Add or replace a ``.param`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "name": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["schematic_path", "name", "value"],
        },
    },
    "suggest_component_placement": {
        "title": "Suggest Component Placement",
        "description": "Suggest the next free grid point to the right of existing parts.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "kind": {"type": "string"}},
            "required": ["schematic_path", "kind"],
        },
    },
}
