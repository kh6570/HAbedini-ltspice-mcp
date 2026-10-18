# In the name of God, the Most Gracious, the Most Merciful
"""Parse the useful sections of an LTspice ``.log`` file."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ltspice_mcp.services._backends.text_decode import read_ltspice_text

if TYPE_CHECKING:
    from pathlib import Path

_MEAS_HEADER = re.compile(r"^Measurement:\s+(\S+)\s*$", re.IGNORECASE)
_MEAS_INLINE = re.compile(r"^([A-Za-z_]\w*):\s+(.+)$")
_FOURIER_THD = re.compile(r"Total Harmonic Distortion:\s+([0-9eE.+-]+)%")
_STEP_LINE = re.compile(r"^\.step\s+(.+)$", re.IGNORECASE)
_OP_LINE = re.compile(r"^(\S+):\s+([+-]?[0-9.eE+-]+)\s+(\S+)\s*$")


def read_log_text(path: Path) -> str:
    """Return the decoded log text."""

    return read_ltspice_text(path)


def _measurement_tables(text: str) -> list[dict[str, object]]:
    measures: list[dict[str, object]] = []
    current_name: str | None = None
    headers: list[str] = []
    for line in text.splitlines():
        header = _MEAS_HEADER.match(line.strip())
        if header:
            current_name = header.group(1)
            headers = []
            measures.append({"name": current_name, "rows": []})
            continue
        if current_name is None or not measures:
            continue
        stripped = line.strip()
        if not stripped:
            current_name = None
            continue
        if stripped.lower().startswith("measurement:"):
            current_name = None
            continue
        parts = stripped.split("\t") if "\t" in stripped else stripped.split()
        if not headers and parts and not parts[0].isdigit():
            headers = parts
            measures[-1]["columns"] = headers
            continue
        if parts and (parts[0].isdigit() or _is_float(parts[0])):
            row = {
                headers[index] if index < len(headers) else str(index): value
                for index, value in enumerate(parts)
            }
            rows = measures[-1]["rows"]
            if isinstance(rows, list):
                rows.append(row)
            continue
        current_name = None
    return measures


def _is_float(token: str) -> bool:
    try:
        float(token)
    except ValueError:
        return False
    return True


def _inline_measures(text: str) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    for line in text.splitlines():
        match = _MEAS_INLINE.match(line.strip())
        if match is None:
            continue
        name, rest = match.group(1), match.group(2)
        if name.lower() in {"measurement", "date", "total"}:
            continue
        if "from" not in rest.lower() and "=" not in rest:
            continue
        found.append({"name": name, "text": rest})
    return found


def parse_measures(text: str) -> list[dict[str, object]]:
    """Return ``.meas`` results from a log."""

    tables = _measurement_tables(text)
    if tables:
        return tables
    return _inline_measures(text)


def parse_steps(text: str) -> list[str]:
    """Return ``.step`` lines."""

    return [match.group(1).strip() for match in _STEP_LINE.finditer(text)]


def parse_fourier(text: str) -> dict[str, object]:
    """Return the Fourier section, including total harmonic distortion when present."""

    thd = [float(match.group(1)) for match in _FOURIER_THD.finditer(text)]
    lines = [line for line in text.splitlines() if "Fourier" in line or "Harmonic" in line]
    return {"thd_percent": thd, "lines": lines[:40]}


def parse_noise(text: str) -> dict[str, object]:
    """Return noise-analysis lines from a log."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if "noise" in line.lower() or "integrated" in line.lower()
    ]
    return {"lines": lines[:40]}


def parse_operating_points(text: str) -> list[dict[str, object]]:
    """Return device operating-point rows from the log."""

    rows: list[dict[str, object]] = []
    capture = False
    for line in text.splitlines():
        if "operating point" in line.lower():
            capture = True
            continue
        if capture and not line.strip():
            if rows:
                break
            continue
        if not capture:
            continue
        match = _OP_LINE.match(line.strip())
        if match:
            rows.append(
                {
                    "name": match.group(1),
                    "value": float(match.group(2)),
                    "unit": match.group(3),
                }
            )
    return rows


def log_summary(path: Path) -> dict[str, object]:
    """Return a bounded summary of one log file."""

    text = read_log_text(path)
    lines = text.splitlines()
    return {
        "path": str(path),
        "line_count": len(lines),
        "succeeded": "total elapsed time" in text.lower(),
        "tail": lines[-30:],
        "measures": parse_measures(text),
        "steps": parse_steps(text),
    }
