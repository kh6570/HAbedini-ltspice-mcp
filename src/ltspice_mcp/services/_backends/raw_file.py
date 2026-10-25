# In the name of God, the Most Gracious, the Most Merciful
"""Clean-room reader for LTspice ``.raw`` files.

The reader reads ASCII (``Values:``) plots and uncompressed binary (``Binary:``) plots directly.
The default GUI file is the LTspice compressed binary. That format stores the
first sample in full. Time is float64. The other traces are float32. Later
samples are deltas. The first byte selects the delta width. The layout matches
XVII 17.0.37 batch output.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from ltspice_mcp.core.exceptions import ParseError

if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray

_BINARY_MARKERS = ("Binary:\r\n", "Binary:\n")
_VALUES_MARKERS = ("Values:\r\n", "Values:\n")
_FLOAT64 = 8
_FLOAT32 = 4


@dataclass
class RawVariable:
    """One column in a raw plot."""

    index: int
    name: str
    kind: str


@dataclass
class RawPlot:
    """One plot from a raw file."""

    title: str
    plotname: str
    flags: frozenset[str]
    variables: tuple[RawVariable, ...]
    real: NDArray[np.float64]
    imag: NDArray[np.float64] | None = None
    encoding: str = "values"

    @property
    def complex_data(self) -> bool:
        """Return True for AC and other complex plots."""

        return self.imag is not None

    def names(self) -> list[str]:
        """Return variable names in column order."""

        return [item.name for item in self.variables]


@dataclass
class RawFile:
    """All plots found in one raw file."""

    plots: list[RawPlot] = field(default_factory=list)

    @property
    def primary(self) -> RawPlot:
        """Return the first plot."""

        if not self.plots:
            raise ParseError("The raw file contains no plots.")
        return self.plots[0]


def _encoding(data: bytes) -> str:
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return "utf-16"
    if len(data) >= 4 and data[1:2] == b"\x00":
        return "utf-16-le"
    return "latin-1"


def _split_header(data: bytes) -> tuple[str, bytes, str]:
    encoding = _encoding(data)
    codec = "utf-16-le" if encoding == "utf-16" else encoding
    markers = [(_BINARY_MARKERS, "binary"), (_VALUES_MARKERS, "values")]
    for group, mode in markers:
        for marker in group:
            token = marker.encode("utf-16-le" if codec == "utf-16-le" else "latin-1")
            index = data.find(token)
            if index < 0:
                continue
            header = data[:index].decode(codec, errors="replace").lstrip("\ufeff")
            return header, data[index + len(token) :], mode
    raise ParseError("Raw file has neither a Binary: nor a Values: section.")


def _header_map(header: str) -> tuple[dict[str, str], list[RawVariable]]:
    meta: dict[str, str] = {}
    variables: list[RawVariable] = []
    in_variables = False
    for raw_line in header.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.lower().startswith("variables:"):
            in_variables = True
            continue
        if in_variables:
            parts = line.split()
            if len(parts) >= 3 and parts[0].isdigit():
                variables.append(RawVariable(int(parts[0]), parts[1], parts[2]))
                continue
            in_variables = False
        if ":" in line:
            key, value = line.split(":", maxsplit=1)
            meta[key.strip().lower()] = value.strip()
    return meta, variables


def _flags(meta: dict[str, str]) -> frozenset[str]:
    return frozenset(part.lower() for part in meta.get("flags", "").split() if part)


def _parse_complex_token(token: str) -> tuple[float, float]:
    if "," not in token:
        return float(token), 0.0
    real_text, imag_text = token.split(",", maxsplit=1)
    return float(real_text), float(imag_text)


def _parse_values(payload: bytes, variables: list[RawVariable], *, complex_data: bool) -> RawPlot:
    text = payload.decode("utf-16-le" if payload[1:2] == b"\x00" else "latin-1", errors="replace")
    rows_real: list[list[float]] = []
    rows_imag: list[list[float]] = []
    current_real: list[float] = []
    current_imag: list[float] = []
    expected = len(variables)

    def _finish() -> None:
        if len(current_real) != expected:
            raise ParseError(f"Values point has {len(current_real)} numbers, expected {expected}.")
        rows_real.append(list(current_real))
        if complex_data:
            rows_imag.append(list(current_imag))

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split()
        if parts[0].isdigit() and len(current_real) in {0, expected}:
            if current_real:
                _finish()
                current_real = []
                current_imag = []
            token = parts[1] if len(parts) > 1 else ""
        else:
            token = parts[0]
        if not token:
            continue
        if complex_data and current_real:
            real_value, imag_value = _parse_complex_token(token)
            current_real.append(real_value)
            current_imag.append(imag_value)
        elif complex_data and not current_real:
            current_real.append(float(token.split(",")[0]))
            current_imag.append(0.0)
        else:
            current_real.append(float(token.split(",")[0]))
            current_imag.append(0.0)
    if current_real:
        _finish()
    if not rows_real:
        raise ParseError("The Values section is empty.")
    real = np.asarray(rows_real, dtype=np.float64)
    imag = np.asarray(rows_imag, dtype=np.float64) if complex_data else None
    return RawPlot("", "", frozenset(), tuple(variables), real, imag, encoding="values")


def _uncompressed_size(n_vars: int, n_points: int, *, complex_data: bool) -> int:
    per_point = _FLOAT64 + (n_vars - 1) * (_FLOAT64 if complex_data else _FLOAT32)
    return per_point * n_points


def _read_uncompressed(
    payload: bytes,
    n_vars: int,
    n_points: int,
    *,
    complex_data: bool,
) -> tuple[NDArray[np.float64], NDArray[np.float64] | None]:
    real = np.zeros((n_points, n_vars), dtype=np.float64)
    imag = np.zeros((n_points, n_vars), dtype=np.float64) if complex_data else None
    offset = 0
    for point in range(n_points):
        real[point, 0] = struct.unpack_from("<d", payload, offset)[0]
        offset += _FLOAT64
        for column in range(1, n_vars):
            if complex_data:
                real[point, column], imag_value = struct.unpack_from("<ff", payload, offset)
                if imag is not None:
                    imag[point, column] = imag_value
                offset += _FLOAT64
            else:
                real[point, column] = struct.unpack_from("<f", payload, offset)[0]
                offset += _FLOAT32
    return real, imag


def _read_delta(payload: bytes, offset: int, previous: float) -> tuple[int, float]:
    """Read one LTspice compressed delta and return the new offset and value.

    The first byte selects the width. A zero nibble at the start means that the rest of
    that byte is a 16-bit-scaled delta after sign extension. ``0xFF`` introduces a
    full-precision absolute sample. Other values are little-endian integer
    deltas. When the top bits are 1, the width is ``1 + (first_byte >> 6)``.
    That width matches XVII compressed batch files.
    """

    if offset >= len(payload):
        raise ParseError("Compressed raw file ended early.")
    first = payload[offset]
    if first == 0xFF:
        if offset + 1 + _FLOAT64 > len(payload):
            raise ParseError("Compressed raw file ended during an absolute sample.")
        value = struct.unpack_from("<d", payload, offset + 1)[0]
        return offset + 1 + _FLOAT64, value
    width_code = first >> 6
    if width_code == 0:
        delta = struct.unpack_from("<b", payload, offset)[0]
        return offset + 1, previous + delta
    width = 1 + width_code
    if offset + width > len(payload):
        raise ParseError("Compressed raw file ended during a delta.")
    if width == 2:
        delta = struct.unpack_from("<h", payload, offset)[0]
    elif width == 3:
        raw = payload[offset : offset + 3] + (b"\xff" if payload[offset + 2] & 0x80 else b"\x00")
        delta = struct.unpack("<i", raw)[0]
    else:
        delta = struct.unpack_from("<i", payload, offset)[0]
    return offset + width, previous + float(delta)


def _read_compressed(
    payload: bytes,
    n_vars: int,
    n_points: int,
) -> tuple[NDArray[np.float64], None]:
    real = np.zeros((n_points, n_vars), dtype=np.float64)
    offset = 0
    if len(payload) < _FLOAT64 + _FLOAT32 * (n_vars - 1):
        raise ParseError("Compressed raw file is too small for its first point.")
    real[0, 0] = struct.unpack_from("<d", payload, offset)[0]
    offset += _FLOAT64
    for column in range(1, n_vars):
        real[0, column] = struct.unpack_from("<f", payload, offset)[0]
        offset += _FLOAT32
    for point in range(1, n_points):
        for column in range(n_vars):
            offset, real[point, column] = _read_delta(
                payload, offset, float(real[point - 1, column])
            )
    return real, None


def _build_plot(
    meta: dict[str, str],
    variables: list[RawVariable],
    real: NDArray[np.float64],
    imag: NDArray[np.float64] | None,
    *,
    encoding: str,
) -> RawPlot:
    return RawPlot(
        title=meta.get("title", ""),
        plotname=meta.get("plotname", ""),
        flags=_flags(meta),
        variables=tuple(variables),
        real=real,
        imag=imag,
        encoding=encoding,
    )


def parse_raw_bytes(data: bytes) -> RawFile:
    """Parse one raw file that is already in memory."""

    header, payload, mode = _split_header(data)
    meta, variables = _header_map(header)
    if not variables:
        raise ParseError("Raw header did not list any variables.")
    try:
        n_points = int(float(meta.get("no. points", "0")))
    except ValueError as exc:
        raise ParseError("Raw header has an invalid point count.") from exc
    flags = _flags(meta)
    complex_data = "complex" in flags
    if mode == "values":
        parsed = _parse_values(payload, variables, complex_data=complex_data)
        return RawFile([_build_plot(meta, variables, parsed.real, parsed.imag, encoding="values")])
    expected = _uncompressed_size(len(variables), n_points, complex_data=complex_data)
    if n_points > 0 and len(payload) == expected:
        real, imag = _read_uncompressed(
            payload, len(variables), n_points, complex_data=complex_data
        )
        return RawFile([_build_plot(meta, variables, real, imag, encoding="binary")])
    if "complex" in flags:
        raise ParseError(
            "Compressed complex raw files are not read. Re-run with -ascii or omit compression."
        )
    real, imag = _read_compressed(payload, len(variables), n_points)
    return RawFile([_build_plot(meta, variables, real, imag, encoding="compressed")])


def load_raw(path: Path) -> RawFile:
    """Load a ``.raw`` file from disk."""

    try:
        return parse_raw_bytes(path.read_bytes())
    except ParseError:
        raise
    except OSError as exc:
        raise ParseError(f"Could not read raw file {path}: {exc}") from exc
