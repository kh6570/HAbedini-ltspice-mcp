# In the name of God, the Most Gracious, the Most Merciful
"""LTspice XVII / 24 command-line adapter.

Documented switches used here are ``-b`` (batch), ``-ascii`` (text raw files),
``-netlist`` (schematic to netlist), and ``-ini`` (private preferences file).
The schematic or netlist path is the final argument. The process working
directory is the file's parent so ``.log``, ``.raw``, and ``.net`` land beside it.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ltspice_mcp.adapters.base import AdapterDescription, SimulationCommand
from ltspice_mcp.core.exceptions import ConvergenceError, SimulationError, ValidationError

if TYPE_CHECKING:
    from pathlib import Path

    from ltspice_mcp.adapters.probe import ProbeResult

LOG_CLASSIFICATION_VERSION = 1

_RESERVED_SWITCHES = frozenset({"-b", "-ascii", "-netlist", "-ini", "-run"})
_PATHLIKE_MARKERS = ("\\", "/", ":")
_SUCCESS_MARKERS = ("total elapsed time",)
_CONVERGENCE_PATTERNS = (
    re.compile(r"time\s*step\s+too\s+small", re.IGNORECASE),
    re.compile(r"singular\s+matrix", re.IGNORECASE),
    re.compile(r"iteration\s+limit", re.IGNORECASE),
    re.compile(r"def\s*con", re.IGNORECASE),
    re.compile(r"failed\s+to\s+converge", re.IGNORECASE),
    re.compile(r"analysis\s+failed", re.IGNORECASE),
)
_FATAL_PATTERNS = (
    re.compile(r"fatal\s+error", re.IGNORECASE),
    re.compile(r"could\s+not\s+open", re.IGNORECASE),
    re.compile(r"unknown\s+subcircuit", re.IGNORECASE),
    re.compile(r"unknown\s+parameter", re.IGNORECASE),
    re.compile(r"missing\s+schematic", re.IGNORECASE),
)


class LtspiceCliV1:
    """Command builder and log classifier for the current LTspice CLI."""

    key = "cli.v1"

    @staticmethod
    def describe(probe: ProbeResult) -> AdapterDescription:
        """Describe this adapter for the probed executable."""

        version = probe.version or "unknown"
        return AdapterDescription(
            key=LtspiceCliV1.key,
            title="LTspice CLI",
            summary=f"Batch LTspice adapter for executable version {version}.",
        )


def describe_ltspice_v1(probe: ProbeResult) -> AdapterDescription:
    """Return the public description of the v1 adapter."""

    return LtspiceCliV1.describe(probe)


def _reject_reserved_switches(extra_switches: tuple[str, ...]) -> None:
    for token in extra_switches:
        head = token.split("=", maxsplit=1)[0].lower()
        if head in _RESERVED_SWITCHES:
            raise ValidationError(f"Switch {token!r} is reserved and cannot be passed through.")
        if any(marker in token for marker in _PATHLIKE_MARKERS):
            raise ValidationError(f"Path-like extra switch is not allowed: {token!r}")


def build_batch_command(
    executable: Path,
    source: Path,
    *,
    ascii_raw: bool = True,
    extra_switches: tuple[str, ...] = (),
) -> SimulationCommand:
    """Build ``LTspice -b [-ascii] <netlist>``.

    XVII 17.0.37 hangs when ``-ini`` is passed, so batch runs use the normal
    user profile. Pass a ``.net`` or ``.cir`` file. An ``.asc`` is netlisted
    first; ``-b`` on a schematic opens the GUI and does not return.
    """

    _reject_reserved_switches(extra_switches)
    if source.suffix.lower() == ".asc":
        raise ValidationError(
            "Batch mode cannot start from a schematic. Netlist the .asc, then run the .net."
        )
    argv = [str(executable), "-b"]
    if ascii_raw:
        argv.append("-ascii")
    argv.extend(extra_switches)
    argv.append(str(source))
    return SimulationCommand(
        argv=tuple(argv),
        cwd=source.parent,
        log_path=source.with_suffix(".log"),
        raw_path=source.with_suffix(".raw"),
        netlist_path=source.with_suffix(".net"),
    )


def build_netlist_command(executable: Path, source: Path) -> SimulationCommand:
    """Build ``LTspice -netlist <schematic>``."""

    argv = [str(executable), "-netlist", str(source)]
    return SimulationCommand(
        argv=tuple(argv),
        cwd=source.parent,
        log_path=source.with_suffix(".log"),
        raw_path=None,
        netlist_path=source.with_suffix(".net"),
    )


def _matching_line(text: str, patterns: tuple[re.Pattern[str], ...]) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.lower().startswith("warning"):
            continue
        for pattern in patterns:
            if pattern.search(stripped):
                return stripped
    return None


def simulation_succeeded(log_text: str) -> bool:
    """Return True when the log contains LTspice's normal completion line."""

    lowered = log_text.lower()
    return any(marker in lowered for marker in _SUCCESS_MARKERS)


def classify_simulation_log(log_text: str, *, return_code: int) -> None:
    """Raise when the log or process status shows a failed analysis."""

    success = simulation_succeeded(log_text)
    fatal = _matching_line(log_text, _FATAL_PATTERNS)
    convergence = _matching_line(log_text, _CONVERGENCE_PATTERNS)
    if convergence is not None and not success:
        raise ConvergenceError(convergence, exit_code=return_code, stderr=log_text[-4000:])
    if fatal is not None and not success:
        raise SimulationError(fatal, exit_code=return_code, stderr=log_text[-4000:])
    if return_code != 0 and not success:
        raise SimulationError(
            f"LTspice exited with status {return_code}.",
            exit_code=return_code,
            stderr=log_text[-4000:] or None,
        )
    if not success:
        tail = log_text.strip().splitlines()[-1] if log_text.strip() else "empty log"
        raise SimulationError(
            f"LTspice did not report completion. Last log line: {tail}",
            exit_code=return_code,
            stderr=log_text[-4000:] or None,
        )
