# In the name of God, the Most Gracious, the Most Merciful
"""Clean-room ``.asy`` symbol reader and writer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ltspice_mcp.core.exceptions import ParseError, ValidationError
from ltspice_mcp.services._backends.asc_document import SCHEMATIC_ENCODING, read_text, write_text

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class AsyPin:
    """One symbol pin."""

    x: int
    y: int
    justification: str = "NONE"
    offset: int = 0
    name: str = ""
    spice_order: int = 0

    def emit(self) -> list[str]:
        """Serialize the pin and its attributes."""

        lines = [f"PIN {self.x} {self.y} {self.justification} {self.offset}"]
        if self.name:
            lines.append(f"PINATTR PinName {self.name}")
        if self.spice_order:
            lines.append(f"PINATTR SpiceOrder {self.spice_order}")
        return lines


@dataclass
class AsySymbol:
    """An in-memory ``.asy`` symbol."""

    version: str = "Version 4"
    symbol_type: str = "CELL"
    graphics: list[str] = field(default_factory=list)
    windows: list[str] = field(default_factory=list)
    attributes: list[tuple[str, str]] = field(default_factory=list)
    pins: list[AsyPin] = field(default_factory=list)

    def attr(self, key: str) -> str | None:
        """Return one attribute."""

        for name, value in self.attributes:
            if name.lower() == key.lower():
                return value
        return None

    def set_attr(self, key: str, value: str) -> None:
        """Insert or replace one attribute."""

        for index, (name, _value) in enumerate(self.attributes):
            if name.lower() == key.lower():
                self.attributes[index] = (name, value)
                return
        self.attributes.append((key, value))

    def emit(self) -> str:
        """Serialize the symbol."""

        lines = [self.version, f"SymbolType {self.symbol_type}"]
        lines.extend(self.graphics)
        lines.extend(self.windows)
        lines.extend(f"SYMATTR {name} {value}" for name, value in self.attributes)
        for pin in self.pins:
            lines.extend(pin.emit())
        return "\n".join(lines) + "\n"


def parse_asy(text: str) -> AsySymbol:
    """Parse one ``.asy`` file."""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines or not lines[0].lower().startswith("version"):
        raise ParseError("An .asy file must start with a Version line.", line=1)
    symbol = AsySymbol(version=lines[0])
    current: AsyPin | None = None
    for line_number, line in enumerate(lines[1:], start=2):
        tokens = line.split()
        keyword = tokens[0].upper()
        if keyword == "SYMBOLTYPE" and len(tokens) >= 2:
            symbol.symbol_type = tokens[1]
            current = None
            continue
        if keyword in {"LINE", "RECTANGLE", "CIRCLE", "ARC", "TEXT"}:
            symbol.graphics.append(line)
            current = None
            continue
        if keyword == "WINDOW":
            symbol.windows.append(line)
            current = None
            continue
        if keyword == "SYMATTR":
            if len(tokens) < 3:
                raise ParseError("SYMATTR line is incomplete.", line=line_number)
            symbol.attributes.append((tokens[1], line.split(None, 2)[2]))
            current = None
            continue
        if keyword == "PIN":
            if len(tokens) < 5:
                raise ParseError("PIN line is incomplete.", line=line_number)
            current = AsyPin(int(tokens[1]), int(tokens[2]), tokens[3], int(tokens[4]))
            symbol.pins.append(current)
            continue
        if keyword == "PINATTR" and current is not None and len(tokens) >= 3:
            if tokens[1].lower() == "pinname":
                current.name = " ".join(tokens[2:])
            elif tokens[1].lower() == "spiceorder":
                current.spice_order = int(tokens[2])
            continue
        symbol.graphics.append(line)
    return symbol


def load_asy(path: Path) -> AsySymbol:
    """Load an ``.asy`` file."""

    return parse_asy(read_text(path))


def save_asy(path: Path, symbol: AsySymbol) -> None:
    """Write an ``.asy`` file."""

    write_text(path, symbol.emit())


def two_pin_box(*, prefix: str, value: str, description: str) -> AsySymbol:
    """Build a simple vertical two-pin cell."""

    symbol = AsySymbol()
    symbol.graphics.extend(
        [
            "LINE Normal 16 16 16 80",
            "RECTANGLE Normal 0 24 32 72",
        ]
    )
    symbol.windows.extend(["WINDOW 0 40 32 Left 2", "WINDOW 3 40 56 Left 2"])
    symbol.attributes.extend(
        [
            ("Prefix", prefix),
            ("Value", value),
            ("Description", description),
        ]
    )
    symbol.pins.extend(
        [
            AsyPin(16, 16, "NONE", 0, "A", 1),
            AsyPin(16, 80, "NONE", 0, "B", 2),
        ]
    )
    return symbol


def encoding_name() -> str:
    """Return the on-disk encoding name."""

    return SCHEMATIC_ENCODING


def require_index(symbol: AsySymbol, index: int) -> None:
    """Raise when a drawing index is outside the graphic list."""

    if index < 0 or index >= len(symbol.graphics):
        raise ValidationError(f"Drawing index {index} is outside 0..{len(symbol.graphics) - 1}.")
