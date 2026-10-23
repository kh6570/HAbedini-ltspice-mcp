# In the name of God, the Most Gracious, the Most Merciful
"""Hash-guarded schematic saves. One edit commits once."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp_app_core.commit import commit_file, content_sha256
from mcp_app_core.errors import ContentConflictError as CoreContentConflictError

from ltspice_mcp.adapters.bridge_client import run_window_guard
from ltspice_mcp.core.exceptions import ContentConflictError, ValidationError
from ltspice_mcp.infra.call_context import current_content_hash
from ltspice_mcp.services._backends.asc_document import (
    SCHEMATIC_ENCODING,
    Schematic,
    read_text,
    write_text,
)
from ltspice_mcp.services._backends.schematic_checks import (
    introduced_findings,
    schematic_findings,
)

if TYPE_CHECKING:
    from pathlib import Path

    from mcp_app_core.checks import CheckFinding


def commit_schematic(
    path: Path,
    schematic: Schematic,
    *,
    previous_findings: tuple[CheckFinding, ...] = (),
    expected_hash: str | None = None,
) -> dict[str, object]:
    """Replace one schematic when its bytes still match the last read.

    A new file is written directly. An existing file uses ``commit_file``.
    The reply lists findings that were already present and findings this call
    introduced. A place-and-wire batch should call this once.
    """

    prior = previous_findings
    content_text = schematic.emit()
    content = content_text.encode(SCHEMATIC_ENCODING)
    disk_text = read_text(path) if path.is_file() else ""

    def write() -> str:
        return _write_bytes(path, content_text, content, expected_hash)

    new_hash, sync = run_window_guard(path, disk_text, content_text, write)
    current = schematic_findings(schematic)
    payload: dict[str, object] = {
        "content_hash": new_hash,
        "findings": {
            "previous": [item.as_dict() for item in prior],
            "introduced": [item.as_dict() for item in introduced_findings(prior, current)],
        },
    }
    if sync is not None:
        payload["window_sync"] = sync
    return payload


def _hash_for(path: Path, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    context = current_content_hash()
    if context is None or not context.digest:
        return None
    resolved = path.resolve()
    if context.path is not None and context.path != resolved:
        return None
    return context.digest


def _remember(path: Path, new_hash: str) -> None:
    context = current_content_hash()
    if context is None:
        return
    resolved = path.resolve()
    if context.path is not None and context.path != resolved:
        return
    context.path = resolved
    context.digest = new_hash


def _write_bytes(path: Path, content_text: str, content: bytes, explicit: str | None) -> str:
    if path.is_file():
        digest = _hash_for(path, explicit)
        if not digest:
            raise ValidationError("Schematic saves require the content hash from the last read.")
        try:
            new_hash = commit_file(path, expected_hash=digest, content=content)
        except CoreContentConflictError as exc:
            raise ContentConflictError(
                str(exc),
                expected_hash=exc.expected_hash,
                actual_hash=exc.actual_hash,
            ) from exc
    else:
        write_text(path, content_text)
        new_hash = content_sha256(content)
    _remember(path, new_hash)
    return new_hash
