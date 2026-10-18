# In the name of God, the Most Gracious, the Most Merciful
"""Retained simulation batches."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING
from uuid import uuid4

from ltspice_mcp.core.exceptions import ArtifactMissingError, BatchConflictError
from ltspice_mcp.services.simulation.operations import run_simulation_service

if TYPE_CHECKING:
    from pathlib import Path

    from ltspice_mcp.infra.config import LTspiceSettings

_BATCHES = "batches"


def _root(settings: LTspiceSettings | None, workspace_root: Path) -> Path:
    base = (
        settings.cache_dir
        if settings is not None and settings.cache_dir is not None
        else workspace_root
    )
    path = base / _BATCHES
    path.mkdir(parents=True, exist_ok=True)
    return path


def _manifest(root: Path, batch_id: str) -> Path:
    return root / batch_id / "manifest.json"


def _load(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise ArtifactMissingError(f"Batch was not found: {path.parent.name}")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise BatchConflictError("Batch manifest is not an object.")
    return {str(key): value for key, value in loaded.items()}


def submit_batch(
    *,
    workspace_root: Path,
    source_path: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Run one schematic and keep a manifest of the artifacts."""

    batch_id = uuid4().hex
    root = _root(settings, workspace_root)
    folder = root / batch_id
    folder.mkdir(parents=True, exist_ok=True)
    result = run_simulation_service(
        workspace_root=workspace_root,
        source_path=source_path,
        settings=settings,
        ltspice_executable=ltspice_executable,
    )
    manifest = {
        "id": batch_id,
        "status": "completed",
        "source_path": source_path,
        "result": result,
    }
    _manifest(root, batch_id).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"batch_id": batch_id, "status": "completed"}


def get_batch_status(
    *,
    workspace_root: Path,
    batch_id: str,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Return a batch manifest summary."""

    data = _load(_manifest(_root(settings, workspace_root), batch_id))
    return {"batch_id": batch_id, "status": data.get("status", "unknown")}


def collect_batch_results(
    *,
    workspace_root: Path,
    batch_id: str,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Return the stored batch result."""

    return _load(_manifest(_root(settings, workspace_root), batch_id))


def cancel_batch(
    *,
    workspace_root: Path,
    batch_id: str,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Mark a batch cancelled. A finished batch stays completed."""

    path = _manifest(_root(settings, workspace_root), batch_id)
    data = _load(path)
    if data.get("status") == "completed":
        return {"batch_id": batch_id, "status": "completed", "cancelled": False}
    data["status"] = "cancelled"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"batch_id": batch_id, "status": "cancelled", "cancelled": True}
