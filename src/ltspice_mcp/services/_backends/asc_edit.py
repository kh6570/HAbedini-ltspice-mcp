# In the name of God, the Most Gracious, the Most Merciful
"""Mutations on an in-memory LTspice schematic."""

from __future__ import annotations

from ltspice_mcp.core.exceptions import ValidationError
from ltspice_mcp.services._backends.asc_document import (
    Flag,
    Schematic,
    Symbol,
    TextItem,
    WindowSpec,
    Wire,
    snap_coord,
)
from ltspice_mcp.services._backends.asc_geometry import (
    assert_rotation,
    canonical_kind,
    connect_nets,
    default_windows,
    primitive_pins,
    symbol_name_for,
    symbol_pins,
)

_ANALYSIS = frozenset({"tran", "ac", "dc", "op", "noise", "tf"})
_DIRECTIVE_Y_START = 480
_DIRECTIVE_Y_STEP = 32


def _require_unique_reference(schematic: Schematic, reference: str) -> None:
    if any(symbol.reference() == reference for symbol in schematic.symbols()):
        raise ValidationError(f"Component reference {reference!r} already exists.")


def _next_directive_origin(schematic: Schematic) -> tuple[int, int]:
    occupied = [item.y for item in schematic.texts()]
    y_pos = _DIRECTIVE_Y_START
    while y_pos in occupied:
        y_pos += _DIRECTIVE_Y_STEP
    return 80, y_pos


def add_primitive(
    schematic: Schematic,
    *,
    kind: str,
    reference: str,
    value: str,
    x: int,
    y: int,
    rotation: str,
) -> dict[str, object]:
    """Place a primitive component or a ground flag."""

    resolved = canonical_kind(kind)
    rotation = assert_rotation(rotation)
    x = snap_coord(x)
    y = snap_coord(y)
    if resolved == "ground":
        schematic.records.append(Flag(x, y, "0"))
        return {"kind": "ground", "net": "0", "x": x, "y": y}
    if not reference:
        raise ValidationError("A component reference is required.")
    _require_unique_reference(schematic, reference)
    symbol = Symbol(name=symbol_name_for(resolved), x=x, y=y, rotation=rotation)
    for attr_id, wx, wy, justification, size in default_windows(resolved):
        symbol.windows.append(WindowSpec(attr_id, wx, wy, justification, size))
    symbol.set_attr("InstName", reference)
    if value:
        symbol.set_attr("Value", value)
    schematic.records.append(symbol)
    pins = [
        {"name": pin.name, "x": pin.x, "y": pin.y, "spice_order": pin.spice_order}
        for pin in primitive_pins(resolved, x=x, y=y, rotation=rotation)
    ]
    return {
        "reference": reference,
        "kind": resolved,
        "symbol": symbol.name,
        "x": x,
        "y": y,
        "rotation": rotation,
        "value": value,
        "pins": pins,
    }


def add_library_symbol(
    schematic: Schematic,
    *,
    symbol_name: str,
    reference: str,
    value: str,
    x: int,
    y: int,
    rotation: str,
) -> dict[str, object]:
    """Place a symbol by its ``.asy`` name."""

    if not symbol_name.strip():
        raise ValidationError("symbol_name is required.")
    if not reference:
        raise ValidationError("A component reference is required.")
    _require_unique_reference(schematic, reference)
    rotation = assert_rotation(rotation)
    symbol = Symbol(
        name=symbol_name.strip(),
        x=snap_coord(x),
        y=snap_coord(y),
        rotation=rotation,
    )
    symbol.windows.append(WindowSpec(0, 16, -16, "Left", 2))
    symbol.windows.append(WindowSpec(3, 16, 16, "Left", 2))
    symbol.set_attr("InstName", reference)
    if value:
        symbol.set_attr("Value", value)
    schematic.records.append(symbol)
    return {
        "reference": reference,
        "symbol": symbol.name,
        "x": symbol.x,
        "y": symbol.y,
        "rotation": rotation,
        "value": value,
    }


def add_wire(schematic: Schematic, *, x1: int, y1: int, x2: int, y2: int) -> dict[str, object]:
    """Add an orthogonal wire."""

    x1, y1, x2, y2 = snap_coord(x1), snap_coord(y1), snap_coord(x2), snap_coord(y2)
    if x1 != x2 and y1 != y2:
        raise ValidationError("Wires must be orthogonal. Change only X or only Y.")
    if (x1, y1) == (x2, y2):
        raise ValidationError("A wire must have nonzero length.")
    wire = Wire(x1, y1, x2, y2)
    if any((item.x1, item.y1, item.x2, item.y2) == (x1, y1, x2, y2) for item in schematic.wires()):
        return {"added": False, "wire": wire.emit(), "reason": "Wire already exists."}
    schematic.records.append(wire)
    return {"added": True, "wire": wire.emit()}


def remove_wire(schematic: Schematic, *, x1: int, y1: int, x2: int, y2: int) -> dict[str, object]:
    """Remove a wire with these endpoints, in either direction."""

    target = {((x1, y1), (x2, y2)), ((x2, y2), (x1, y1))}
    kept: list[object] = []
    removed = 0
    for record in schematic.records:
        if isinstance(record, Wire) and (record.endpoints()[0], record.endpoints()[1]) in target:
            removed += 1
            continue
        kept.append(record)
    schematic.records = kept  # type: ignore[assignment]
    if removed == 0:
        raise ValidationError("Wire was not found.")
    return {"removed": removed}


def add_net_label(schematic: Schematic, *, x: int, y: int, name: str) -> dict[str, object]:
    """Place a FLAG net label."""

    if not name.strip():
        raise ValidationError("A net name is required.")
    x, y = snap_coord(x), snap_coord(y)
    for flag in schematic.flags():
        if (flag.x, flag.y) == (x, y):
            flag.name = name.strip()
            return {"x": x, "y": y, "name": flag.name, "replaced": True}
    schematic.records.append(Flag(x, y, name.strip()))
    return {"x": x, "y": y, "name": name.strip(), "replaced": False}


def remove_net_label(schematic: Schematic, *, x: int, y: int, name: str = "") -> dict[str, object]:
    """Remove a flag at a point, optionally matching its name."""

    kept: list[object] = []
    removed = 0
    for record in schematic.records:
        if isinstance(record, Flag) and record.x == x and record.y == y:
            if name and record.name != name:
                kept.append(record)
                continue
            removed += 1
            continue
        kept.append(record)
    schematic.records = kept  # type: ignore[assignment]
    if removed == 0:
        raise ValidationError("Net label was not found.")
    return {"removed": removed}


def add_junction(schematic: Schematic, *, x: int, y: int) -> dict[str, object]:
    """Split any wire that passes through this grid point.

    LTspice has no junction keyword. A connection exists only where endpoints meet,
    so a wire that merely crosses a coordinate is split there.
    """

    x, y = snap_coord(x), snap_coord(y)
    point = (x, y)
    rebuilt: list[object] = []
    splits = 0
    for record in schematic.records:
        if not isinstance(record, Wire):
            rebuilt.append(record)
            continue
        horizontal = record.y1 == record.y2 == y and min(record.x1, record.x2) < x < max(
            record.x1, record.x2
        )
        vertical = record.x1 == record.x2 == x and min(record.y1, record.y2) < y < max(
            record.y1, record.y2
        )
        if horizontal or vertical:
            rebuilt.append(Wire(record.x1, record.y1, x, y))
            rebuilt.append(Wire(x, y, record.x2, record.y2))
            splits += 1
            continue
        rebuilt.append(record)
    schematic.records = rebuilt  # type: ignore[assignment]
    return {
        "x": x,
        "y": y,
        "splits": splits,
        "note": "LTspice junctions are implicit. The wire was split so the point connects.",
        "connected": point in connect_nets(schematic),
    }


def remove_junction(schematic: Schematic, *, x: int, y: int) -> dict[str, object]:
    """Report that a junction cannot be deleted as its own object."""

    meeting = 0
    for wire in schematic.wires():
        if (wire.x1, wire.y1) == (x, y) or (wire.x2, wire.y2) == (x, y):
            meeting += 1
    return {
        "removed": False,
        "wires_meeting": meeting,
        "reason": "LTspice stores no junction object. Delete a wire to open the connection.",
    }


def upsert_directive(
    schematic: Schematic,
    text: str,
    *,
    x: int | None = None,
    y: int | None = None,
    replace_command: str | None = None,
    comment_other_analyses: bool = False,
) -> dict[str, object]:
    """Insert or replace a SPICE directive."""

    body = text.strip()
    if body.startswith("!"):
        body = body[1:].strip()
    if not body.startswith("."):
        body = f".{body}"
    command = body[1:].split(maxsplit=1)[0].lower()
    if comment_other_analyses and command in _ANALYSIS:
        for item in schematic.texts():
            if item.is_directive and item.command() in _ANALYSIS and item.command() != command:
                item.text = ";" + item.body()
    replaced = False
    for item in schematic.texts():
        if item.command() == (replace_command or command) and (
            item.is_directive or item.text.startswith(";")
        ):
            item.text = f"!{body}"
            replaced = True
            break
    if not replaced:
        origin_x, origin_y = _next_directive_origin(schematic)
        schematic.records.append(
            TextItem(
                x if x is not None else origin_x,
                y if y is not None else origin_y,
                "Left",
                2,
                f"!{body}",
            )
        )
    return {"directive": body, "replaced": replaced}


def remove_directive(schematic: Schematic, text: str) -> dict[str, object]:
    """Remove a directive whose body contains ``text``."""

    needle = text.strip().lstrip("!").lower()
    kept: list[object] = []
    removed = 0
    for record in schematic.records:
        if isinstance(record, TextItem) and needle in record.text.lower():
            removed += 1
            continue
        kept.append(record)
    schematic.records = kept  # type: ignore[assignment]
    if removed == 0:
        raise ValidationError(f"Directive containing {text!r} was not found.")
    return {"removed": removed}


def set_component_value(schematic: Schematic, reference: str, value: str) -> dict[str, object]:
    """Set SYMATTR Value."""

    symbol = schematic.find_symbol(reference)
    symbol.set_attr("Value", value)
    return {"reference": reference, "value": value}


def set_component_parameters(
    schematic: Schematic, reference: str, spice_line: str, spice_line2: str = ""
) -> dict[str, object]:
    """Set SpiceLine and optional SpiceLine2."""

    symbol = schematic.find_symbol(reference)
    symbol.set_attr("SpiceLine", spice_line)
    if spice_line2:
        symbol.set_attr("SpiceLine2", spice_line2)
    return {"reference": reference, "spice_line": spice_line, "spice_line2": spice_line2}


def set_element_model(schematic: Schematic, reference: str, model: str) -> dict[str, object]:
    """Set SpiceModel and, when Value is empty, the model value."""

    symbol = schematic.find_symbol(reference)
    symbol.set_attr("SpiceModel", model)
    if symbol.attr("Value") in {None, ""}:
        symbol.set_attr("Value", model)
    return {"reference": reference, "model": model}


def rename_reference(schematic: Schematic, reference: str, new_reference: str) -> dict[str, object]:
    """Rename InstName."""

    if not new_reference.strip():
        raise ValidationError("new_reference is required.")
    if new_reference != reference:
        _require_unique_reference(schematic, new_reference)
    symbol = schematic.find_symbol(reference)
    symbol.set_attr("InstName", new_reference)
    return {"reference": new_reference, "previous": reference}


def remove_component(schematic: Schematic, reference: str) -> dict[str, object]:
    """Remove a component by InstName."""

    schematic.find_symbol(reference)
    schematic.records = [
        record
        for record in schematic.records
        if not (isinstance(record, Symbol) and record.reference() == reference)
    ]
    return {"removed": reference}


def move_component(
    schematic: Schematic,
    reference: str,
    *,
    x: int,
    y: int,
    rotation: str = "",
) -> dict[str, object]:
    """Move a component and drag wire endpoints that sat on its old pins."""

    symbol = schematic.find_symbol(reference)
    old_pins = symbol_pins(symbol)
    new_rotation = assert_rotation(rotation) if rotation else symbol.rotation
    new_x, new_y = snap_coord(x), snap_coord(y)
    kind_pins_before = [(pin.x, pin.y) for pin in old_pins]
    symbol.x = new_x
    symbol.y = new_y
    symbol.rotation = new_rotation
    new_pins = [(pin.x, pin.y) for pin in symbol_pins(symbol)]
    moved_endpoints = 0
    if kind_pins_before and len(kind_pins_before) == len(new_pins):
        mapping = dict(zip(kind_pins_before, new_pins, strict=True))
        for wire in schematic.wires():
            start = (wire.x1, wire.y1)
            end = (wire.x2, wire.y2)
            if start in mapping:
                wire.x1, wire.y1 = mapping[start]
                moved_endpoints += 1
            if end in mapping:
                wire.x2, wire.y2 = mapping[end]
                moved_endpoints += 1
        for flag in schematic.flags():
            if (flag.x, flag.y) in mapping:
                flag.x, flag.y = mapping[(flag.x, flag.y)]
    return {
        "reference": reference,
        "x": new_x,
        "y": new_y,
        "rotation": new_rotation,
        "moved_endpoints": moved_endpoints,
    }


def component_summary(symbol: Symbol) -> dict[str, object]:
    """Return a JSON summary of one symbol."""

    return {
        "reference": symbol.reference(),
        "symbol": symbol.name,
        "x": symbol.x,
        "y": symbol.y,
        "rotation": symbol.rotation,
        "value": symbol.attr("Value") or "",
        "spice_model": symbol.attr("SpiceModel") or "",
        "spice_line": symbol.attr("SpiceLine") or "",
        "spice_line2": symbol.attr("SpiceLine2") or "",
        "attributes": dict(symbol.attributes),
        "pins": [
            {"name": pin.name, "x": pin.x, "y": pin.y, "spice_order": pin.spice_order}
            for pin in symbol_pins(symbol)
        ],
    }
