# In the name of God, the Most Gracious, the Most Merciful
"""Decode LTspice text artifacts that may be UTF-16 or Windows-1252."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def decode_ltspice_text(data: bytes) -> str:
    """Decode a log, netlist, or raw header."""

    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
        return data.decode("utf-16")
    if len(data) >= 4 and data[1:2] == b"\x00" and data[3:4] == b"\x00":
        return data.decode("utf-16-le")
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1", errors="replace")


def read_ltspice_text(path: Path) -> str:
    """Read one LTspice text artifact."""

    return decode_ltspice_text(path.read_bytes())
