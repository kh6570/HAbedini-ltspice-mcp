# In the name of God, the Most Gracious, the Most Merciful
"""Sandboxed workspace writes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ltspice_mcp.services._shared.paths import resolve_workspace_path

if TYPE_CHECKING:
    from pathlib import Path


def write_workspace_text_file(
    *,
    workspace_root: Path,
    relative_path: str,
    content: str,
) -> dict[str, object]:
    """Write a text file inside the workspace."""

    path = resolve_workspace_path(relative_path, workspace_root=workspace_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"path": str(path), "bytes": len(content.encode("utf-8"))}
