# In the name of God, the Most Gracious, the Most Merciful
"""Small simulator-neutral topology notes."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import TYPE_CHECKING

from ltspice_mcp.core.exceptions import ValidationError
from ltspice_mcp.services._shared.paths import resolve_workspace_path

if TYPE_CHECKING:
    from pathlib import Path

_REQUIRED = ("id", "title", "summary", "equations")


def _bundled() -> list[dict[str, object]]:
    root = files("ltspice_mcp.data.topology")
    blocks: list[dict[str, object]] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if not path.name.endswith(".json"):
            continue
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            blocks.append({str(key): value for key, value in loaded.items()})
    return blocks


def _contributed(workspace_root: Path) -> list[dict[str, object]]:
    folder = workspace_root / "topology" / "contributions"
    if not folder.is_dir():
        return []
    blocks: list[dict[str, object]] = []
    for path in sorted(folder.glob("*.json")):
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            blocks.append({str(key): value for key, value in loaded.items()})
    return blocks


def _all(workspace_root: Path) -> list[dict[str, object]]:
    return _bundled() + _contributed(workspace_root)


def list_topology_blocks(*, workspace_root: Path) -> dict[str, object]:
    """List topology notes."""

    return {
        "blocks": [
            {"id": item.get("id"), "title": item.get("title")} for item in _all(workspace_root)
        ]
    }


def describe_topology_block(*, workspace_root: Path, block_id: str) -> dict[str, object]:
    """Return one topology note."""

    for block in _all(workspace_root):
        if block.get("id") == block_id:
            return block
    raise ValidationError(f"Topology block {block_id!r} was not found.")


def search_topology_blocks(*, workspace_root: Path, query: str) -> dict[str, object]:
    """Search titles and summaries."""

    needle = query.lower()
    hits = [
        block
        for block in _all(workspace_root)
        if needle in str(block.get("title", "")).lower()
        or needle in str(block.get("summary", "")).lower()
    ]
    return {"matches": hits}


def validate_topology_contribution(*, workspace_root: Path, payload: str) -> dict[str, object]:
    """Check that a contribution JSON object has the required keys."""

    del workspace_root
    loaded = json.loads(payload)
    if not isinstance(loaded, dict):
        raise ValidationError("Topology contribution must be a JSON object.")
    missing = [key for key in _REQUIRED if key not in loaded]
    return {"ok": not missing, "missing": missing}


def ingest_topology_contribution(*, workspace_root: Path, payload: str) -> dict[str, object]:
    """Store a validated contribution under the workspace."""

    checked = validate_topology_contribution(workspace_root=workspace_root, payload=payload)
    if not checked["ok"]:
        raise ValidationError(f"Contribution is missing {checked['missing']}.")
    loaded = json.loads(payload)
    if not isinstance(loaded, dict):
        raise ValidationError("Topology contribution must be a JSON object.")
    block_id = str(loaded["id"])
    destination = resolve_workspace_path(
        f"topology/contributions/{block_id}.json", workspace_root=workspace_root
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(loaded, indent=2) + "\n", encoding="utf-8")
    return {"path": str(destination), "id": block_id}


def describe_topology_authoring_support(*, workspace_root: Path) -> dict[str, object]:
    """Describe the topology note format."""

    del workspace_root
    return {
        "required": list(_REQUIRED),
        "note": "Topology notes are textbook relationships. They are not schematics.",
    }
