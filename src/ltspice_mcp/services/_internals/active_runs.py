# In the name of God, the Most Gracious, the Most Merciful
"""In-process handles for simulations that ``cancel_run`` can stop."""

from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import subprocess

_LOCK = Lock()
_RUNS: dict[str, subprocess.Popen[str]] = {}


def register_run(key: str, process: subprocess.Popen[str]) -> None:
    """Remember a simulation that is in progress."""

    with _LOCK:
        _RUNS[key] = process


def pop_run(key: str) -> subprocess.Popen[str] | None:
    """Forget a finished simulation and return its process, if any."""

    with _LOCK:
        return _RUNS.pop(key, None)


def cancel_run(key: str) -> subprocess.Popen[str] | None:
    """Return the process for ``key``. Keep the record until the caller stops the process."""

    with _LOCK:
        return _RUNS.get(key)
