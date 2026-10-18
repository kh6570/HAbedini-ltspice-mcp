# In the name of God, the Most Gracious, the Most Merciful
"""Clean-room reader and writer for LTspice ``.asc`` schematics.

``.asc`` files are Windows-1252 text. This module reads and writes them as
Latin-1, which preserves every byte LTspice stores, including the micro sign
at ``0xB5``. Newly authored values use ASCII ``u`` rather than ``µ``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ltspice_mcp.core.exceptions import ParseError, ValidationError

if TYPE_CHECKING:
    from pathlib import Path

SCHEMATIC_ENCODING = "latin-1"
_GRID = 16
_ROTATIONS = frozenset({"R0", "R90", "R180", "R270", "M0", "M90", "M180", "M270"})
_VERSION_RE = re.compile(r"^Version\s+4(?:\.\d+)?$", re.IGNORECASE)
_SHEET_RE = re.compile(r"^SHEET\s+(\d+)\s+(-?\d+)\s+(-?\d+)\s*$", re.IGNORECASE)


def read_text(path: Path) -> str:
    """Read a schematic or symbol without a UTF-8 round trip."""

    return path.read_bytes().decode(SCHEMATIC_ENCODING)


def write_text(path: Path, text: str) -> None:
    """Write schematic text as Latin-1, which keeps Windows-1252 bytes intact."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode(SCHEMATIC_ENCODING))


def snap_coord(value: int, *, grid: int = _GRID) -> int:
    """Snap one coordinate onto the LTspice grid."""

    return int(round(value / grid) * grid)


@dataclass
class WindowSpec:
    """Where one symbol attribute is drawn."""

    attr_id: int
    x: int
    y: int
    justification: str
    size: int

    def emit(self) -> str:
        """Serialize this window."""

        return f"WINDOW {self.attr_id} {self.x} {self.y} {self.justification} {self.size}"


@dataclass
class Symbol:
    """One placed component."""

    name: str
    x: int
    y: int
    rotation: str
    windows: list[WindowSpec] = field(default_factory=list)
    attributes: list[tuple[str, str]] = field(default_factory=list)

    def attr(self, key: str) -> str | None:
        """Return one attribute value, matching names without case."""

        for name, value in self.attributes:
            if name.lower() == key.lower():
                return value
        return None

    def set_attr(self, key: str, value: str) -> None:
        """Insert or replace one attribute, preserving the original key spelling."""

        for index, (name, _value) in enumerate(self.attributes):
            if name.lower() == key.lower():
                self.attributes[index] = (name, value)
                return
        self.attributes.append((key, value))

    def reference(self) -> str:
        """Return InstName or an empty string."""

        return self.attr("InstName") or ""

    def emit(self) -> list[str]:
        """Serialize the symbol block."""

        lines = [f"SYMBOL {self.name} {self.x} {self.y} {self.rotation}"]
        lines.extend(window.emit() for window in self.windows)
        lines.extend(f"SYMATTR {name} {value}" for name, value in self.attributes)
        return lines


@dataclass
class Wire:
    """One wire segment."""

    x1: int
    y1: int
    x2: int
    y2: int

    def emit(self) -> str:
        """Serialize this wire."""

        return f"WIRE {self.x1} {self.y1} {self.x2} {self.y2}"

    def endpoints(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return the two endpoints."""

        return (self.x1, self.y1), (self.x2, self.y2)


@dataclass
class Flag:
    """A net label or ground flag."""

    x: int
    y: int
    name: str

    def emit(self) -> str:
        """Serialize this flag."""

        return f"FLAG {self.x} {self.y} {self.name}"


@dataclass
class TextItem:
    """A comment or a SPICE directive."""

    x: int
    y: int
    justification: str
    size: int
    text: str

    @property
    def is_directive(self) -> bool:
        """Return True when LTspice will execute this text."""

        return self.text.startswith("!")

    def body(self) -> str:
        """Return the directive text without the ``!`` or ``;`` prefix."""

        raw = self.text[1:] if self.text.startswith(("!", ";")) else self.text
        return raw.strip()

    def command(self) -> str:
        """Return the first SPICE word, such as ``tran`` or ``meas``."""

        body = self.body()
        if body.startswith("."):
            body = body[1:]
        token = body.split(maxsplit=1)[0] if body else ""
        return token.lower()

    def emit(self) -> str:
        """Serialize this text item."""

        return f"TEXT {self.x} {self.y} {self.justification} {self.size} {self.text}"


@dataclass
class Graphic:
    """A non-electrical drawing primitive stored on the schematic."""

    kind: str
    args: tuple[str, ...]

    def emit(self) -> str:
        """Serialize this graphic."""

        return " ".join((self.kind, *self.args))


@dataclass
class IoPin:
    """A hierarchical sheet pin."""

    x: int
    y: int
    direction: str

    def emit(self) -> str:
        """Serialize this pin."""

        return f"IOPIN {self.x} {self.y} {self.direction}"


@dataclass
class RawLine:
    """A line this editor preserves but does not interpret."""

    text: str

    def emit(self) -> str:
        """Return the original line."""

        return self.text


Record = Symbol | Wire | Flag | TextItem | Graphic | IoPin | RawLine


@dataclass
class Schematic:
    """An in-memory ``.asc`` document."""

    version: str = "Version 4"
    sheet: int = 1
    width: int = 880
    height: int = 680
    records: list[Record] = field(default_factory=list)

    def symbols(self) -> list[Symbol]:
        """Return placed components in file order."""

        return [item for item in self.records if isinstance(item, Symbol)]

    def wires(self) -> list[Wire]:
        """Return wire segments in file order."""

        return [item for item in self.records if isinstance(item, Wire)]

    def flags(self) -> list[Flag]:
        """Return net flags in file order."""

        return [item for item in self.records if isinstance(item, Flag)]

    def texts(self) -> list[TextItem]:
        """Return text and directives in file order."""

        return [item for item in self.records if isinstance(item, TextItem)]

    def find_symbol(self, reference: str) -> Symbol:
        """Return the component with this InstName."""

        matches = [item for item in self.symbols() if item.reference() == reference]
        if not matches:
            raise ValidationError(f"Component {reference!r} was not found.")
        if len(matches) > 1:
            raise ValidationError(f"Component reference {reference!r} is duplicated.")
        return matches[0]

    def emit(self) -> str:
        """Serialize the schematic."""

        lines = [
            self.version,
            f"SHEET {self.sheet} {self.width} {self.height}",
        ]
        for record in self.records:
            if isinstance(record, Symbol):
                lines.extend(record.emit())
            else:
                lines.append(record.emit())
        return "\n".join(lines) + "\n"


def _tokens(line: str) -> list[str]:
    return line.split()


def _parse_int(token: str, *, line_number: int) -> int:
    try:
        return int(token)
    except ValueError as exc:
        raise ParseError(f"Expected an integer, got {token!r}.", line=line_number) from exc


def _parse_window(tokens: list[str], *, line_number: int) -> WindowSpec:
    if len(tokens) < 6:
        raise ParseError("WINDOW line is incomplete.", line=line_number)
    return WindowSpec(
        attr_id=_parse_int(tokens[1], line_number=line_number),
        x=_parse_int(tokens[2], line_number=line_number),
        y=_parse_int(tokens[3], line_number=line_number),
        justification=tokens[4],
        size=_parse_int(tokens[5], line_number=line_number),
    )


def _parse_symbol_start(tokens: list[str], *, line_number: int) -> Symbol:
    if len(tokens) < 5:
        raise ParseError("SYMBOL line is incomplete.", line=line_number)
    rotation = tokens[-1]
    if rotation not in _ROTATIONS:
        raise ParseError(f"Unsupported symbol orientation {rotation!r}.", line=line_number)
    name = " ".join(tokens[1:-3])
    return Symbol(
        name=name,
        x=_parse_int(tokens[-3], line_number=line_number),
        y=_parse_int(tokens[-2], line_number=line_number),
        rotation=rotation,
    )


def _parse_text(line: str, *, line_number: int) -> TextItem:
    tokens = _tokens(line)
    if len(tokens) < 6:
        raise ParseError("TEXT line is incomplete.", line=line_number)
    content = line.split(None, 5)[5]
    return TextItem(
        x=_parse_int(tokens[1], line_number=line_number),
        y=_parse_int(tokens[2], line_number=line_number),
        justification=tokens[3],
        size=_parse_int(tokens[4], line_number=line_number),
        text=content,
    )


def parse_schematic(text: str) -> Schematic:
    """Parse one ``.asc`` document."""

    lines = text.splitlines()
    if not lines or _VERSION_RE.match(lines[0].strip()) is None:
        raise ParseError("An .asc file must start with Version 4 or Version 4.1.", line=1)
    schematic = Schematic(version=lines[0].strip())
    sheet_seen = False
    index = 1
    while index < len(lines):
        line = lines[index].strip()
        line_number = index + 1
        if not line:
            index += 1
            continue
        tokens = _tokens(line)
        keyword = tokens[0].upper()
        if keyword == "SHEET":
            match = _SHEET_RE.match(line)
            if match is None:
                raise ParseError("SHEET line is incomplete.", line=line_number)
            if not sheet_seen:
                schematic.sheet = int(match.group(1))
                schematic.width = int(match.group(2))
                schematic.height = int(match.group(3))
                sheet_seen = True
            else:
                schematic.records.append(RawLine(line))
            index += 1
            continue
        if keyword == "WIRE":
            if len(tokens) != 5:
                raise ParseError("WIRE line is incomplete.", line=line_number)
            schematic.records.append(
                Wire(
                    _parse_int(tokens[1], line_number=line_number),
                    _parse_int(tokens[2], line_number=line_number),
                    _parse_int(tokens[3], line_number=line_number),
                    _parse_int(tokens[4], line_number=line_number),
                )
            )
            index += 1
            continue
        if keyword == "FLAG":
            if len(tokens) < 4:
                raise ParseError("FLAG line is incomplete.", line=line_number)
            schematic.records.append(
                Flag(
                    _parse_int(tokens[1], line_number=line_number),
                    _parse_int(tokens[2], line_number=line_number),
                    " ".join(tokens[3:]),
                )
            )
            index += 1
            continue
        if keyword == "TEXT":
            schematic.records.append(_parse_text(line, line_number=line_number))
            index += 1
            continue
        if keyword == "IOPIN":
            if len(tokens) != 4:
                raise ParseError("IOPIN line is incomplete.", line=line_number)
            schematic.records.append(
                IoPin(
                    _parse_int(tokens[1], line_number=line_number),
                    _parse_int(tokens[2], line_number=line_number),
                    tokens[3],
                )
            )
            index += 1
            continue
        if keyword in {"LINE", "RECTANGLE", "CIRCLE", "ARC", "DATAFLAG"}:
            schematic.records.append(Graphic(keyword, tuple(tokens[1:])))
            index += 1
            continue
        if keyword == "SYMBOL":
            symbol = _parse_symbol_start(tokens, line_number=line_number)
            index += 1
            while index < len(lines):
                follower = lines[index].strip()
                if not follower:
                    index += 1
                    continue
                follower_tokens = _tokens(follower)
                follower_key = follower_tokens[0].upper()
                if follower_key == "WINDOW":
                    symbol.windows.append(_parse_window(follower_tokens, line_number=index + 1))
                    index += 1
                    continue
                if follower_key == "SYMATTR":
                    if len(follower_tokens) < 3:
                        raise ParseError("SYMATTR line is incomplete.", line=index + 1)
                    value = follower.split(None, 2)[2]
                    symbol.attributes.append((follower_tokens[1], value))
                    index += 1
                    continue
                break
            schematic.records.append(symbol)
            continue
        schematic.records.append(RawLine(line))
        index += 1
    if not sheet_seen:
        raise ParseError("An .asc file must contain a SHEET line.", line=2)
    return schematic


def load_schematic(path: Path) -> Schematic:
    """Load an ``.asc`` file from disk."""

    try:
        return parse_schematic(read_text(path))
    except ParseError:
        raise
    except OSError as exc:
        raise ParseError(f"Could not read schematic {path}: {exc}") from exc


def save_schematic(path: Path, schematic: Schematic) -> None:
    """Write an ``.asc`` file."""

    write_text(path, schematic.emit())


def blank_schematic(*, version: str = "Version 4") -> Schematic:
    """Return an empty sheet."""

    return Schematic(version=version)
