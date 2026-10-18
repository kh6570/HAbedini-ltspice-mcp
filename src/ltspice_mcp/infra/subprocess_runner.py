# In the name of God, the Most Gracious, the Most Merciful
"""Subprocess helper for short-lived LTspice invocations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mcp_app_core.process import kill_process_tree as _core_kill
from mcp_app_core.process import run_command as _core_run

from ltspice_mcp.core.exceptions import SimulationError, SimulationTimeoutError

if TYPE_CHECKING:
    import subprocess
    from collections.abc import Callable
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Completed child-process summary."""

    command: tuple[str, ...]
    return_code: int
    stdout: str
    stderr: str


def _kill_process_tree(process: subprocess.Popen[str]) -> None:
    """Stop a child and any processes it spawned."""

    _core_kill(process)


def run_command(
    command: list[str],
    *,
    cwd: Path,
    timeout_s: float | None,
    on_start: Callable[[subprocess.Popen[str]], None] | None = None,
) -> CommandResult:
    """Run one command, enforce the timeout, and return captured text."""

    completed = _core_run(
        command,
        cwd=cwd,
        timeout_s=timeout_s,
        timeout_error=SimulationTimeoutError,
        start_error=SimulationError,
        on_start=on_start,
    )
    return CommandResult(
        command=completed.command,
        return_code=completed.return_code,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
