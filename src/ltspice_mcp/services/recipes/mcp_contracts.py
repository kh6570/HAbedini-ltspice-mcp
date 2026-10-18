# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "describe_reference_circuit_recipe": {
        "title": "Describe Reference Circuit Recipe",
        "description": "Describe one reference circuit.",
        "input_schema": {
            "type": "object",
            "properties": {"recipe_id": {"type": "string"}},
            "required": ["recipe_id"],
        },
    },
    "list_reference_circuit_recipes": {
        "title": "List Reference Circuit Recipes",
        "description": "List bundled reference circuits.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    "materialize_recipe": {
        "title": "Materialize Recipe",
        "description": "Write a recipe schematic into the workspace.",
        "input_schema": {
            "type": "object",
            "properties": {"recipe_id": {"type": "string"}, "destination_path": {"type": "string"}},
            "required": ["recipe_id", "destination_path"],
        },
    },
}
