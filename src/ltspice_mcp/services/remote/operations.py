# In the name of God, the Most Gracious, the Most Merciful
"""Background simulation sessions on this machine.

There is no remote LTspice service. A session runs the local executable and
keeps the artifact paths for a later download step.
"""

from __future__ import annotations

import json
import threading
from typing import TYPE_CHECKING
from uuid import uuid4

from ltspice_mcp.core.exceptions import ArtifactMissingError
from ltspice_mcp.services.simulation.operations import run_simulation_service

if TYPE_CHECKING:
    from pathlib import Path

    from ltspice_mcp.infra.config import LTspiceSettings

_SESSIONS: dict[str, dict[str, object]] = {}
_LOCK = threading.Lock()


def _folder(settings: LTspiceSettings | None, workspace_root: Path, session_id: str) -> Path:
    base = (
        settings.cache_dir
        if settings is not None and settings.cache_dir is not None
        else workspace_root
    )
    path = base / "remote" / session_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def submit_remote_simulation(
    *,
    workspace_root: Path,
    source_path: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Start a background local simulation and return a session id."""

    session_id = uuid4().hex
    with _LOCK:
        _SESSIONS[session_id] = {"status": "running", "result": None, "error": None}

    def _worker() -> None:
        try:
            result = run_simulation_service(
                workspace_root=workspace_root,
                source_path=source_path,
                settings=settings,
                ltspice_executable=ltspice_executable,
            )
            status = "completed"
            error = None
        except Exception as exc:
            result = None
            status = "failed"
            error = str(exc)
        with _LOCK:
            _SESSIONS[session_id] = {"status": status, "result": result, "error": error}
        folder = _folder(settings, workspace_root, session_id)
        folder.joinpath("status.json").write_text(
            json.dumps(_SESSIONS[session_id], indent=2, default=str),
            encoding="utf-8",
        )

    threading.Thread(target=_worker, daemon=True).start()
    return {"session_id": session_id, "status": "running"}


def poll_remote_run(
    *,
    workspace_root: Path,
    session_id: str,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Return the status of a background session."""

    with _LOCK:
        current = _SESSIONS.get(session_id)
    if current is None:
        path = _folder(settings, workspace_root, session_id) / "status.json"
        if not path.is_file():
            raise ArtifactMissingError(f"Remote session {session_id!r} was not found.")
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            return {"session_id": session_id, "status": loaded.get("status")}
    return {"session_id": session_id, "status": None if current is None else current.get("status")}


def download_remote_artifacts(
    *,
    workspace_root: Path,
    session_id: str,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Return artifact paths recorded for a finished session."""

    with _LOCK:
        current = _SESSIONS.get(session_id)
    result = None if current is None else current.get("result")
    if not isinstance(result, dict):
        path = _folder(settings, workspace_root, session_id) / "status.json"
        if path.is_file():
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                result = loaded.get("result")
    if not isinstance(result, dict):
        raise ArtifactMissingError("Session has no artifacts yet.")
    return {
        "session_id": session_id,
        "log_path": result.get("log_path"),
        "raw_path": result.get("raw_path"),
        "netlist_path": result.get("netlist_path"),
    }


def close_remote_session(
    *,
    workspace_root: Path,
    session_id: str,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Drop a session from memory. Files on disk are left in place."""

    del workspace_root, settings
    with _LOCK:
        _SESSIONS.pop(session_id, None)
    return {"session_id": session_id, "closed": True}
