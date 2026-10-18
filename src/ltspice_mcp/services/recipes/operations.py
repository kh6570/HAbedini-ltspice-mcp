# In the name of God, the Most Gracious, the Most Merciful
"""Reference-circuit recipes shipped with the server."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import TYPE_CHECKING

from ltspice_mcp.core.exceptions import ArtifactMissingError
from ltspice_mcp.services.schematic.operations import materialize_reference_circuit

if TYPE_CHECKING:
    from pathlib import Path


def _catalog() -> list[dict[str, object]]:
    root = files("ltspice_mcp.data.recipes")
    recipes: list[dict[str, object]] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        manifest = path.joinpath("recipe.json")
        if manifest.is_file():
            loaded = json.loads(manifest.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                recipes.append({str(key): value for key, value in loaded.items()})
    return recipes


def list_reference_circuit_recipes(*, workspace_root: Path) -> dict[str, object]:
    """List bundled reference circuits."""

    del workspace_root
    return {"recipes": _catalog()}


def describe_reference_circuit_recipe(*, workspace_root: Path, recipe_id: str) -> dict[str, object]:
    """Describe one reference circuit."""

    del workspace_root
    for recipe in _catalog():
        if recipe.get("id") == recipe_id:
            return recipe
    raise ArtifactMissingError(f"Recipe {recipe_id!r} was not found.")


def materialize_recipe(
    *,
    workspace_root: Path,
    recipe_id: str,
    destination_path: str,
) -> dict[str, object]:
    """Write a recipe schematic into the workspace."""

    describe_reference_circuit_recipe(workspace_root=workspace_root, recipe_id=recipe_id)
    return materialize_reference_circuit(
        workspace_root=workspace_root,
        recipe_id=recipe_id,
        destination_path=destination_path,
    )
