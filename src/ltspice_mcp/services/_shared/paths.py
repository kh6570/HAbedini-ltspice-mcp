# In the name of God, the Most Gracious, the Most Merciful
"""Workspace path checks. The rules live in mcp-app-core."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp_app_core.paths import resolve_output_path as _resolve_output_path
from mcp_app_core.paths import resolve_workspace_path as _resolve_workspace_path
from mcp_app_core.paths import validate_existing_file as _validate_existing_file

from ltspice_mcp.core.exceptions import (
    ArtifactMissingError,
    SandboxViolationError,
    ValidationError,
)

if TYPE_CHECKING:
    from pathlib import Path


def resolve_workspace_path(raw_path: str | Path, *, workspace_root: Path) -> Path:
    """Resolve a relative or absolute path inside the configured workspace root."""

    return _resolve_workspace_path(
        raw_path, workspace_root=workspace_root, sandbox_error=SandboxViolationError
    )


def validate_existing_file(
    raw_path: str | Path,
    *,
    workspace_root: Path,
    suffixes: tuple[str, ...] = (),
) -> Path:
    """Resolve and validate a file that is already in the workspace root."""

    return _validate_existing_file(
        raw_path,
        workspace_root=workspace_root,
        suffixes=suffixes,
        sandbox_error=SandboxViolationError,
        validation_error=ValidationError,
        missing_error=ArtifactMissingError,
    )


def resolve_output_path(
    raw_path: str | Path | None,
    *,
    workspace_root: Path,
    default: Path,
    suffixes: tuple[str, ...],
) -> Path:
    """Resolve one writable output path inside the workspace."""

    resolved = _resolve_output_path(
        raw_path,
        workspace_root=workspace_root,
        default=default,
        suffixes=suffixes,
        sandbox_error=SandboxViolationError,
        validation_error=ValidationError,
    )
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved
