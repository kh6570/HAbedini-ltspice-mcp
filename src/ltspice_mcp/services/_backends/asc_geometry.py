# In the name of God, the Most Gracious, the Most Merciful
"""Pin geometry and net connectivity for LTspice symbols.

The standard LTspice symbol files publish the pin offsets.
The files include ``res.asy``, ``cap.asy``, and the other primitive cells.
Orientation follows LTspice's rule: rotate clockwise first, then mirror horizontally for ``M*``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ltspice_mcp.core.exceptions import ValidationError

if TYPE_CHECKING:
    from ltspice_mcp.services._backends.asc_document import Schematic, Symbol, Wire

_GRID = 16

# A kind value maps to a symbol name, a SPICE prefix, and the pin tuples.
# Each pin tuple contains x, y, the pin name, and the SPICE order.
_PRIMITIVES: dict[str, tuple[str, str, tuple[tuple[int, int, str, int], ...]]] = {
    "resistor": ("res", "R", ((16, 16, "A", 1), (16, 96, "B", 2))),
    "capacitor": ("cap", "C", ((16, 0, "A", 1), (16, 64, "B", 2))),
    "inductor": ("ind", "L", ((16, 16, "A", 1), (16, 96, "B", 2))),
    "diode": ("diode", "D", ((16, 0, "+", 1), (16, 64, "-", 2))),
    "voltage_source": ("voltage", "V", ((0, 16, "+", 1), (0, 96, "-", 2))),
    "current_source": ("current", "I", ((0, 0, "+", 1), (0, 80, "-", 2))),
    "behavioral": ("bv", "B", ((0, 16, "+", 1), (0, 96, "-", 2))),
    "nmos": ("nmos", "MN", ((48, 0, "D", 1), (0, 80, "G", 2), (48, 96, "S", 3))),
    "pmos": ("pmos", "MP", ((48, 0, "D", 1), (0, 80, "G", 2), (48, 96, "S", 3))),
    "npn": ("npn", "QN", ((64, 0, "C", 1), (0, 48, "B", 2), (64, 96, "E", 3))),
    "pnp": ("pnp", "QP", ((64, 0, "C", 1), (0, 48, "B", 2), (64, 96, "E", 3))),
    "opamp": (
        r"OpAmps\opamp",
        "X",
        ((-32, 48, "invin", 1), (-32, 80, "noninvin", 2), (32, 64, "out", 3)),
    ),
}

_KIND_ALIASES = {
    "res": "resistor",
    "r": "resistor",
    "cap": "capacitor",
    "c": "capacitor",
    "ind": "inductor",
    "l": "inductor",
    "d": "diode",
    "voltage": "voltage_source",
    "v": "voltage_source",
    "current": "current_source",
    "i": "current_source",
    "bv": "behavioral",
    "b": "behavioral",
    "gnd": "ground",
    "ground": "ground",
}


@dataclass(frozen=True, slots=True)
class PinPlacement:
    """One symbol pin in schematic coordinates."""

    name: str
    spice_order: int
    x: int
    y: int


def canonical_kind(kind: str) -> str:
    """Map a caller kind or symbol name onto a primitive key."""

    kind_key = kind.strip().lower().replace(" ", "_")
    kind_key = _KIND_ALIASES.get(kind_key, kind_key)
    if kind_key == "ground" or kind_key in _PRIMITIVES:
        return kind_key
    raise ValidationError(
        f"Unknown component kind {kind!r}. "
        "Use a primitive kind or add_library_component for a symbol name."
    )


def symbol_name_for(kind: str) -> str:
    """Return the ``.asy`` name that a primitive kind places."""

    resolved = canonical_kind(kind)
    if resolved == "ground":
        return "flag"
    return _PRIMITIVES[resolved][0]


def prefix_for(kind: str) -> str:
    """Return the LTspice symbol prefix for a primitive kind."""

    resolved = canonical_kind(kind)
    if resolved == "ground":
        return ""
    return _PRIMITIVES[resolved][1]


def _rotate(x: int, y: int, rotation: str) -> tuple[int, int]:
    if rotation == "R0":
        return x, y
    if rotation == "R90":
        return y, -x
    if rotation == "R180":
        return -x, -y
    if rotation == "R270":
        return -y, x
    if rotation == "M0":
        return -x, y
    if rotation == "M90":
        return -y, -x
    if rotation == "M180":
        return x, -y
    if rotation == "M270":
        return y, x
    raise ValidationError(f"Unsupported orientation {rotation!r}.")


def primitive_pins(kind: str, *, x: int, y: int, rotation: str) -> tuple[PinPlacement, ...]:
    """Return world-coordinate pins for a primitive placement."""

    resolved = canonical_kind(kind)
    if resolved == "ground":
        return (PinPlacement("0", 1, x, y),)
    pins: list[PinPlacement] = []
    for pin_x, pin_y, name, order in _PRIMITIVES[resolved][2]:
        dx, dy = _rotate(pin_x, pin_y, rotation)
        pins.append(PinPlacement(name, order, x + dx, y + dy))
    return tuple(sorted(pins, key=lambda pin: pin.spice_order))


def symbol_kind(symbol: Symbol) -> str | None:
    """Return the primitive kind for a placed symbol, if it is one of the built-ins."""

    normalized = symbol.name.replace("/", "\\").lower()
    for kind, (name, _prefix, _pins) in _PRIMITIVES.items():
        if normalized == name.replace("/", "\\").lower():
            return kind
    return None


def symbol_pins(symbol: Symbol) -> tuple[PinPlacement, ...]:
    """Return pins for a placed primitive. Library symbols return an empty tuple."""

    kind = symbol_kind(symbol)
    if kind is None:
        return ()
    return primitive_pins(kind, x=symbol.x, y=symbol.y, rotation=symbol.rotation)


def _on_segment(point: tuple[int, int], wire: Wire) -> bool:
    px, py = point
    x1, y1, x2, y2 = wire.x1, wire.y1, wire.x2, wire.y2
    horizontal = x1 == x2 == px and min(y1, y2) <= py <= max(y1, y2)
    vertical = y1 == y2 == py and min(x1, x2) <= px <= max(x1, x2)
    return horizontal or vertical


class _UnionFind:
    def __init__(self) -> None:
        self._parent: dict[tuple[int, int], tuple[int, int]] = {}

    def add(self, point: tuple[int, int]) -> None:
        self._parent.setdefault(point, point)

    def find(self, point: tuple[int, int]) -> tuple[int, int]:
        self.add(point)
        parent = self._parent[point]
        if parent != point:
            self._parent[point] = self.find(parent)
        return self._parent[point]

    def union(self, left: tuple[int, int], right: tuple[int, int]) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self._parent[right_root] = left_root


def connect_nets(schematic: Schematic) -> dict[tuple[int, int], str]:
    """Map every electrical point to a net name.

    Ground flags force net ``0``. Other flags name their connected component.
    Unlabeled nodes receive ``N001`` style names in first-seen order.
    """

    points: list[tuple[int, int]] = []
    for wire in schematic.wires():
        points.extend(wire.endpoints())
    for flag in schematic.flags():
        points.append((flag.x, flag.y))
    for symbol in schematic.symbols():
        points.extend((pin.x, pin.y) for pin in symbol_pins(symbol))

    unique = list(dict.fromkeys(points))
    forest = _UnionFind()
    for point in unique:
        forest.add(point)
    for wire in schematic.wires():
        forest.union((wire.x1, wire.y1), (wire.x2, wire.y2))
        for point in unique:
            if _on_segment(point, wire):
                forest.union(point, (wire.x1, wire.y1))

    names: dict[tuple[int, int], str] = {}
    for flag in schematic.flags():
        root = forest.find((flag.x, flag.y))
        current = names.get(root)
        if flag.name == "0" or current is None:
            names[root] = flag.name
    counter = 1
    resolved: dict[tuple[int, int], str] = {}
    for point in unique:
        root = forest.find(point)
        if root not in names:
            names[root] = f"N{counter:03d}"
            counter += 1
        resolved[point] = names[root]
    return resolved


def default_windows(kind: str) -> list[tuple[int, int, int, str, int]]:
    """Return InstName and Value window offsets for a primitive."""

    resolved = canonical_kind(kind)
    if resolved in {"voltage_source", "current_source", "behavioral"}:
        return [(0, 24, 16, "Left", 2), (3, 24, 96, "Left", 2)]
    if resolved == "capacitor":
        return [(0, 24, 8, "Left", 2), (3, 24, 56, "Left", 2)]
    if resolved == "diode":
        return [(0, 24, 0, "Left", 2), (3, 24, 64, "Left", 2)]
    if resolved == "opamp":
        return [(0, 0, 32, "Left", 2)]
    return [(0, 36, 40, "Left", 2), (3, 36, 76, "Left", 2)]


def assert_rotation(rotation: str) -> str:
    """Validate an orientation token."""

    if rotation not in {"R0", "R90", "R180", "R270", "M0", "M90", "M180", "M270"}:
        raise ValidationError("Orientation must be R0, R90, R180, R270, M0, M90, M180, or M270.")
    return rotation


def grid() -> int:
    """Return the schematic grid in LTspice coordinate units."""

    return _GRID
