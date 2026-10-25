# In the name of God, the Most Gracious, the Most Merciful
"""Launch the LTspice GUI. Window sync uses the 26.1 bridge after you enable that bridge."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from ltspice_mcp.adapters.probe import probe_ltspice
from ltspice_mcp.core.exceptions import BackendUnavailableError, UnsupportedError
from ltspice_mcp.infra.config import LTspiceSettings
from ltspice_mcp.services._shared.paths import validate_existing_file

if TYPE_CHECKING:
    from pathlib import Path

_PROCESSES: dict[str, subprocess.Popen[bytes]] = {}


def describe_live_gui_support(
    *,
    workspace_root: Path,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Describe GUI launch and the optional LTspice 26 window sync."""

    del workspace_root
    probe = probe_ltspice(settings or LTspiceSettings())
    if probe.message_bridge:
        return {
            "open_schematic": True,
            "command_channel": True,
            "launch_only": False,
            "bridge_present": True,
            "window_sync": "opt-in",
            "note": (
                "ltspice-mcp-bridge.exe is present for LTspice 26.1 or newer. "
                "Window sync stays off until LTSPICE_WINDOW_SYNC=1. "
                "When it is on, a save attaches only to a schematic you already opened, "
                "does not start a hidden LTspice, and asks you to save first if that "
                "window differs from the file on disk. After the file is saved, the new "
                "text is pushed as one undo step."
            ),
        }
    return {
        "open_schematic": True,
        "command_channel": False,
        "launch_only": True,
        "bridge_present": False,
        "window_sync": "unavailable",
        "note": (
            "This LTspice build launches the schematic in a visible window. "
            "Batch simulation stays on disk. Window sync needs LTspice 26.1 or newer "
            "with ltspice-mcp-bridge.exe beside LTspice.exe."
        ),
    }


def _unsupported(action: str) -> dict[str, object]:
    raise UnsupportedError(
        f"{action} is unavailable. Edit the .asc and run a batch simulation. "
        "LTspice 26.1 window sync is opt-in and does not accept free-form commands."
    )


def open_schematic_in_gui(
    *,
    workspace_root: Path,
    schematic_path: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Launch LTspice on a schematic without ``-b``."""

    path = validate_existing_file(schematic_path, workspace_root=workspace_root, suffixes=(".asc",))
    exe = ltspice_executable
    if exe is None or not exe.is_file():
        if settings is None:
            raise BackendUnavailableError("LTspice settings were not provided.")
        probed = probe_ltspice(settings)
        exe = probed.executable if probed.exists else None
    if exe is None:
        raise BackendUnavailableError("LTspice is not installed.")
    process = subprocess.Popen([str(exe), str(path)])  # noqa: S603
    _PROCESSES[str(path)] = process
    return {"pid": process.pid, "path": str(path)}


def close_live_gui_session(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Stop a GUI process this server launched."""

    path = validate_existing_file(schematic_path, workspace_root=workspace_root, suffixes=(".asc",))
    process = _PROCESSES.pop(str(path), None)
    if process is None or process.poll() is not None:
        return {"closed": False, "reason": "No GUI process is tracked for that schematic."}
    process.terminate()
    return {"closed": True, "pid": process.pid}


def refresh_schematic_in_gui(
    *,
    workspace_root: Path,
    schematic_path: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Close and reopen the schematic so the GUI reloads the file."""

    close_live_gui_session(workspace_root=workspace_root, schematic_path=schematic_path)
    return open_schematic_in_gui(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        settings=settings,
        ltspice_executable=ltspice_executable,
    )


def poll_live_gui_session(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Report that the server does not support a poll of a GUI session."""

    del workspace_root, schematic_path
    return _unsupported("poll_live_gui_session")


def poll_live_gui_session_events(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Report that the server does not support GUI events."""

    del workspace_root, schematic_path
    return _unsupported("poll_live_gui_session_events")


def send_live_gui_session_command(
    *, workspace_root: Path, schematic_path: str, command: str
) -> dict[str, object]:
    """Report that the server does not support GUI commands."""

    del workspace_root, schematic_path, command
    return _unsupported("send_live_gui_session_command")
