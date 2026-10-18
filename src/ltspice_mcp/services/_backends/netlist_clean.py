# In the name of God, the Most Gracious, the Most Merciful
"""Clean-room netlist for primitive LTspice schematics.

Official netlists still come from ``XVIIx64.exe -netlist``. This renderer covers
the built-in primitives so unit tests and offline inspection do not need the GUI.
"""

from __future__ import annotations

from ltspice_mcp.services._backends.asc_document import Schematic, TextItem
from ltspice_mcp.services._backends.asc_geometry import (
    connect_nets,
    prefix_for,
    symbol_kind,
    symbol_pins,
)


def _net_at(
    point: tuple[int, int],
    nets: dict[tuple[int, int], str],
    *,
    fallback: str,
) -> str:
    return nets.get(point, fallback)


def render_clean_room_netlist(schematic: Schematic) -> str:
    """Render a SPICE netlist from primitive symbols, wires, flags, and directives."""

    nets = connect_nets(schematic)
    lines = ["* ltspice-mcp clean-room netlist"]
    for symbol in schematic.symbols():
        kind = symbol_kind(symbol)
        reference = symbol.reference() or "X?"
        pins = symbol_pins(symbol)
        if kind is None or not pins:
            lines.append(f"* skipped {reference} ({symbol.name}): not a built-in primitive")
            continue
        prefix = prefix_for(kind)
        nodes = [
            _net_at((pin.x, pin.y), nets, fallback=f"NC_{pin.x}_{pin.y}")
            for pin in sorted(pins, key=lambda pin: pin.spice_order)
        ]
        value = symbol.attr("Value") or symbol.attr("SpiceModel") or prefix
        extras = [
            part
            for part in (symbol.attr("SpiceLine") or "", symbol.attr("SpiceLine2") or "")
            if part
        ]
        card = " ".join([reference, *nodes, value, *extras])
        lines.append(card)
    for item in schematic.texts():
        if isinstance(item, TextItem) and item.is_directive:
            lines.append(item.body())
    lines.append(".end")
    return "\n".join(lines) + "\n"
