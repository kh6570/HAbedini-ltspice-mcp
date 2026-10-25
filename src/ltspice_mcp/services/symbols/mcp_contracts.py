# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "add_hierarchical_block": {
        "title": "Add Hierarchical Block",
        "description": "Create a child sheet with In/Out pins and place it on the parent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "block_name": {"type": "string"},
                "reference": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
            },
            "required": ["schematic_path", "block_name", "reference"],
        },
    },
    "create_asy_symbol": {
        "title": "Create Asy Symbol",
        "description": "Write a two-pin ``.asy`` symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "output_path": {"type": "string"},
                "prefix": {"type": "string"},
                "value": {"type": "string"},
                "description": {"type": "string"},
            },
            "required": ["output_path"],
        },
    },
    "describe_mixed_signal_support": {
        "title": "Describe Mixed Signal Support",
        "description": "State the mixed-signal design tasks that LTspice can do. State the design tasks that LTspice cannot do.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "describe_protocol_support": {
        "title": "Describe Protocol Support",
        "description": "State that the I2C and SPI scaffolds here are behavioral circuits for instruction.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "scaffold_behavioral_subcircuit": {
        "title": "Scaffold Behavioral Subcircuit",
        "description": "Write a schematic whose only active device is a behavioral source.",
        "input_schema": {
            "type": "object",
            "properties": {"output_path": {"type": "string"}, "expression": {"type": "string"}},
            "required": ["output_path"],
        },
    },
    "scaffold_i2c_device": {
        "title": "Scaffold I2c Device",
        "description": "Write a behavioral sketch of an I2C open-drain pull-up, not a protocol engine.",
        "input_schema": {
            "type": "object",
            "properties": {"output_path": {"type": "string"}},
            "required": ["output_path"],
        },
    },
    "scaffold_spi_device": {
        "title": "Scaffold Spi Device",
        "description": "Write a behavioral sketch of a SPI data latch, not a protocol engine.",
        "input_schema": {
            "type": "object",
            "properties": {"output_path": {"type": "string"}},
            "required": ["output_path"],
        },
    },
}
