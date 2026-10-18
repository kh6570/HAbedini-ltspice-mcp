# In the name of God, the Most Gracious, the Most Merciful
"""Bundled workflow instructions."""

from __future__ import annotations

from importlib.resources import files
from typing import TYPE_CHECKING

from ltspice_mcp.core.exceptions import ArtifactMissingError

if TYPE_CHECKING:
    from pathlib import Path


def _instruction_text(name: str) -> str:
    root = files("ltspice_mcp.data.instructions")
    target = root.joinpath(f"{name}.md")
    if not target.is_file():
        raise ArtifactMissingError(f"Instruction {name!r} was not found.")
    return target.read_text(encoding="utf-8")


def list_workflow_instructions(*, workspace_root: Path) -> dict[str, object]:
    """List bundled workflow notes."""

    del workspace_root
    root = files("ltspice_mcp.data.instructions")
    names = sorted(
        path.name.removesuffix(".md") for path in root.iterdir() if path.name.endswith(".md")
    )
    return {"instructions": names}


def read_workflow_instruction(*, workspace_root: Path, name: str) -> dict[str, object]:
    """Read one bundled workflow note."""

    del workspace_root
    return {"name": name, "text": _instruction_text(name)}
