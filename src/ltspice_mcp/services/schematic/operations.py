# In the name of God, the Most Gracious, the Most Merciful
"""Schematic use cases."""

from __future__ import annotations

import zipfile
from io import BytesIO

import matplotlib

matplotlib.use("Agg", force=True)
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
from mcp_app_core.commit import file_content_sha256
from mcp_app_core.images import ImageResult

from ltspice_mcp.adapters.probe import probe_ltspice, schematic_version_line
from ltspice_mcp.core.exceptions import ValidationError
from ltspice_mcp.services._backends.asc_document import (
    Schematic,
    TextItem,
    load_schematic,
)
from ltspice_mcp.services._backends.asc_edit import (
    add_junction,
    add_library_symbol,
    add_net_label,
    add_primitive,
    add_wire,
    component_summary,
    move_component,
    remove_component,
    remove_directive,
    remove_junction,
    remove_net_label,
    remove_wire,
    rename_reference,
    set_component_parameters,
    set_component_value,
    set_element_model,
    upsert_directive,
)
from ltspice_mcp.services._backends.asc_geometry import connect_nets, symbol_pins
from ltspice_mcp.services._backends.asy_document import (
    AsyPin,
    load_asy,
    require_index,
    save_asy,
    two_pin_box,
)
from ltspice_mcp.services._backends.schematic_checks import (
    check_payload,
    netlist_findings,
    schematic_findings,
)
from ltspice_mcp.services._backends.schematic_commit import commit_schematic
from ltspice_mcp.services._backends.starters import build_named
from ltspice_mcp.services._shared.paths import (
    resolve_output_path,
    resolve_workspace_path,
    validate_existing_file,
)

if TYPE_CHECKING:
    from pathlib import Path

    from mcp_app_core.checks import CheckFinding

    from ltspice_mcp.infra.config import LTspiceSettings

_LAYOUTS = {
    "divider": "Left-to-right resistive divider on the 16-unit grid.",
    "rc": "Series resistor and shunt capacitor low-pass.",
    "buck": "Open-loop buck power stage with a pulsed source and a diode.",
}


def _load(
    workspace_root: Path, schematic_path: str
) -> tuple[Path, Schematic, tuple[CheckFinding, ...]]:
    path = validate_existing_file(schematic_path, workspace_root=workspace_root, suffixes=(".asc",))
    schematic = load_schematic(path)
    return path, schematic, schematic_findings(schematic)


def _existing_findings(path: Path) -> tuple[CheckFinding, ...]:
    if not path.is_file():
        return ()
    return schematic_findings(load_schematic(path))


def _save(
    path: Path,
    schematic: Schematic,
    *,
    previous: tuple[CheckFinding, ...],
) -> dict[str, object]:
    return commit_schematic(path, schematic, previous_findings=previous)


def _version(settings: LTspiceSettings | None) -> str:
    if settings is None:
        return "Version 4"
    return schematic_version_line(probe_ltspice(settings).version)


def create_schematic(
    *,
    workspace_root: Path,
    schematic_path: str,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Create an empty schematic."""

    path = resolve_output_path(
        schematic_path,
        workspace_root=workspace_root,
        default=workspace_root / "untitled.asc",
        suffixes=(".asc",),
    )
    schematic = Schematic(version=_version(settings))
    saved = _save(path, schematic, previous=_existing_findings(path))
    return {"path": str(path), "version": schematic.version, **saved}


def create_starter_schematic(
    *,
    workspace_root: Path,
    schematic_path: str,
    kind: str = "divider",
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Create a divider, RC, or buck starter schematic."""

    path = resolve_output_path(
        schematic_path,
        workspace_root=workspace_root,
        default=workspace_root / f"{kind}.asc",
        suffixes=(".asc",),
    )
    schematic = build_named(kind, _version(settings))
    saved = _save(path, schematic, previous=_existing_findings(path))
    return {
        "path": str(path),
        "kind": kind,
        "components": len(schematic.symbols()),
        **saved,
    }


def save_schematic_as(
    *,
    workspace_root: Path,
    schematic_path: str,
    destination_path: str,
) -> dict[str, object]:
    """Copy a schematic to a new path."""

    path, schematic, _source_findings = _load(workspace_root, schematic_path)
    destination = resolve_output_path(
        destination_path,
        workspace_root=workspace_root,
        default=path.with_name(path.stem + "-copy.asc"),
        suffixes=(".asc",),
    )
    saved = _save(destination, schematic, previous=_existing_findings(destination))
    return {"path": str(destination), "source_hash": file_content_sha256(path), **saved}


def add_component(
    *,
    workspace_root: Path,
    schematic_path: str,
    kind: str,
    reference: str,
    value: str = "",
    x: int = 0,
    y: int = 0,
    rotation: str = "R0",
) -> dict[str, object]:
    """Place a primitive component."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    placed = add_primitive(
        schematic,
        kind=kind,
        reference=reference,
        value=value,
        x=x,
        y=y,
        rotation=rotation,
    )
    placed.update(_save(path, schematic, previous=previous))
    placed["path"] = str(path)
    return placed


def add_library_component(
    *,
    workspace_root: Path,
    schematic_path: str,
    symbol_name: str,
    reference: str,
    value: str = "",
    x: int = 0,
    y: int = 0,
    rotation: str = "R0",
) -> dict[str, object]:
    """Place a library symbol by name."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    placed = add_library_symbol(
        schematic,
        symbol_name=symbol_name,
        reference=reference,
        value=value,
        x=x,
        y=y,
        rotation=rotation,
    )
    placed.update(_save(path, schematic, previous=previous))
    placed["path"] = str(path)
    return placed


def add_wire_service(
    *,
    workspace_root: Path,
    schematic_path: str,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
) -> dict[str, object]:
    """Add a wire. The tool module exposes this operation as ``add_wire``."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = add_wire(schematic, x1=x1, y1=y1, x2=x2, y2=y2)
    result.update(_save(path, schematic, previous=previous))
    result["path"] = str(path)
    return result


def remove_wire_service(
    *,
    workspace_root: Path,
    schematic_path: str,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
) -> dict[str, object]:
    """Remove a wire."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = remove_wire(schematic, x1=x1, y1=y1, x2=x2, y2=y2)
    result.update(_save(path, schematic, previous=previous))
    return result


def add_junction_service(
    *, workspace_root: Path, schematic_path: str, x: int, y: int
) -> dict[str, object]:
    """Split a wire so a coordinate becomes a junction."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = add_junction(schematic, x=x, y=y)
    result.update(_save(path, schematic, previous=previous))
    return result


def remove_junction_service(
    *, workspace_root: Path, schematic_path: str, x: int, y: int
) -> dict[str, object]:
    """Explain that LTspice junctions are implicit."""

    _path, schematic, _previous = _load(workspace_root, schematic_path)
    return remove_junction(schematic, x=x, y=y)


def add_net_label_service(
    *, workspace_root: Path, schematic_path: str, x: int, y: int, name: str
) -> dict[str, object]:
    """Add a net label."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = add_net_label(schematic, x=x, y=y, name=name)
    result.update(_save(path, schematic, previous=previous))
    return result


def remove_net_label_service(
    *,
    workspace_root: Path,
    schematic_path: str,
    x: int,
    y: int,
    name: str = "",
) -> dict[str, object]:
    """Remove a net label."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = remove_net_label(schematic, x=x, y=y, name=name)
    result.update(_save(path, schematic, previous=previous))
    return result


def add_instruction(
    *,
    workspace_root: Path,
    schematic_path: str,
    text: str,
    x: int = 80,
    y: int = 400,
) -> dict[str, object]:
    """Add a SPICE directive or a comment."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    if text.strip().startswith(";"):
        schematic.records.append(TextItem(x, y, "Left", 2, text.strip()))
        saved = _save(path, schematic, previous=previous)
        return {"text": text.strip(), "comment": True, **saved}
    result = upsert_directive(schematic, text, x=x, y=y)
    result.update(_save(path, schematic, previous=previous))
    return result


def remove_instruction(
    *, workspace_root: Path, schematic_path: str, text: str
) -> dict[str, object]:
    """Remove a directive or a comment that contains ``text``."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = remove_directive(schematic, text)
    result.update(_save(path, schematic, previous=previous))
    return result


def set_parameter(
    *, workspace_root: Path, schematic_path: str, name: str, value: str
) -> dict[str, object]:
    """Add or replace a ``.param`` directive."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = upsert_directive(schematic, f".param {name}={value}", replace_command="param")
    result.update(_save(path, schematic, previous=previous))
    return result


def set_component_value_service(
    *, workspace_root: Path, schematic_path: str, reference: str, value: str
) -> dict[str, object]:
    """Set a component value."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = set_component_value(schematic, reference, value)
    result.update(_save(path, schematic, previous=previous))
    return result


def set_component_parameters_service(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    spice_line: str,
    spice_line2: str = "",
) -> dict[str, object]:
    """Set SpiceLine attributes."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = set_component_parameters(schematic, reference, spice_line, spice_line2)
    result.update(_save(path, schematic, previous=previous))
    return result


def set_element_model_service(
    *, workspace_root: Path, schematic_path: str, reference: str, model: str
) -> dict[str, object]:
    """Set a component model."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = set_element_model(schematic, reference, model)
    result.update(_save(path, schematic, previous=previous))
    return result


def set_component_position(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    x: int,
    y: int,
    rotation: str = "",
) -> dict[str, object]:
    """Move a component and wires that ended on its pins."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = move_component(schematic, reference, x=x, y=y, rotation=rotation)
    result.update(_save(path, schematic, previous=previous))
    return result


def rename_component_reference(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    new_reference: str,
) -> dict[str, object]:
    """Rename InstName."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = rename_reference(schematic, reference, new_reference)
    result.update(_save(path, schematic, previous=previous))
    return result


def remove_component_service(
    *, workspace_root: Path, schematic_path: str, reference: str
) -> dict[str, object]:
    """Remove a component."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    result = remove_component(schematic, reference)
    result.update(_save(path, schematic, previous=previous))
    return result


def suggest_component_placement(
    *, workspace_root: Path, schematic_path: str, kind: str
) -> dict[str, object]:
    """Suggest the next free grid point to the right of the parts on the schematic."""

    _path, schematic, _previous = _load(workspace_root, schematic_path)
    xs = [symbol.x for symbol in schematic.symbols()] or [0]
    return {"kind": kind, "x": max(xs) + 160, "y": 80, "rotation": "R0", "grid": 16}


def list_components(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """List placed components."""

    path, schematic, _previous = _load(workspace_root, schematic_path)
    return {
        "path": str(path),
        "content_hash": file_content_sha256(path),
        "components": [component_summary(symbol) for symbol in schematic.symbols()],
    }


def read_component(
    *, workspace_root: Path, schematic_path: str, reference: str
) -> dict[str, object]:
    """Read one component."""

    path, schematic, _previous = _load(workspace_root, schematic_path)
    summary = component_summary(schematic.find_symbol(reference))
    summary["content_hash"] = file_content_sha256(path)
    return summary


def inspect_schematic(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Summarize a schematic."""

    path, schematic, _previous = _load(workspace_root, schematic_path)
    directives = [item.body() for item in schematic.texts() if item.is_directive]
    return {
        "path": str(path),
        "content_hash": file_content_sha256(path),
        "version": schematic.version,
        "sheet": {"number": schematic.sheet, "width": schematic.width, "height": schematic.height},
        "counts": {
            "symbols": len(schematic.symbols()),
            "wires": len(schematic.wires()),
            "flags": len(schematic.flags()),
            "directives": len(directives),
        },
        "directives": directives,
        "flags": [{"x": flag.x, "y": flag.y, "name": flag.name} for flag in schematic.flags()],
    }


def read_net_connectivity(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Return primitive pin-to-net connectivity."""

    path, schematic, _previous = _load(workspace_root, schematic_path)
    nets = connect_nets(schematic)
    components: list[dict[str, object]] = []
    for symbol in schematic.symbols():
        pins = []
        for pin in symbol_pins(symbol):
            pins.append(
                {
                    "name": pin.name,
                    "net": nets.get((pin.x, pin.y), f"NC_{pin.x}_{pin.y}"),
                    "x": pin.x,
                    "y": pin.y,
                }
            )
        components.append({"reference": symbol.reference(), "symbol": symbol.name, "pins": pins})
    named = sorted({flag.name for flag in schematic.flags()})
    return {
        "components": components,
        "flag_names": named,
        "content_hash": file_content_sha256(path),
    }


def check_schematic(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Report structural problems. Do not start LTspice."""

    path, schematic, _previous = _load(workspace_root, schematic_path)
    result = check_payload(schematic_findings(schematic))
    result["path"] = str(path)
    result["content_hash"] = file_content_sha256(path)
    return result


def check_netlist(*, workspace_root: Path, netlist_path: str) -> dict[str, object]:
    """Report structural problems in a ``.net`` or ``.cir`` file."""

    path = validate_existing_file(
        netlist_path,
        workspace_root=workspace_root,
        suffixes=(".net", ".cir"),
    )
    text = path.read_text(encoding="latin-1", errors="replace")
    result = check_payload(netlist_findings(text))
    result["path"] = str(path)
    result["content_hash"] = file_content_sha256(path)
    return result


def compare_schematics(
    *, workspace_root: Path, left_path: str, right_path: str
) -> dict[str, object]:
    """Compare component values between two schematics."""

    _left, left, _left_findings = _load(workspace_root, left_path)
    _right, right, _right_findings = _load(workspace_root, right_path)
    left_map = {symbol.reference(): symbol.attr("Value") or "" for symbol in left.symbols()}
    right_map = {symbol.reference(): symbol.attr("Value") or "" for symbol in right.symbols()}
    changes = [
        {"reference": key, "left": left_map.get(key), "right": right_map.get(key)}
        for key in sorted(set(left_map) | set(right_map))
        if left_map.get(key) != right_map.get(key)
    ]
    return {
        "changed": changes,
        "left_wires": len(left.wires()),
        "right_wires": len(right.wires()),
    }


def render_schematic_image(
    *,
    workspace_root: Path,
    schematic_path: str,
    output_path: str = "",
) -> dict[str, object]:
    """Draw a simple schematic preview."""

    path, schematic, _previous = _load(workspace_root, schematic_path)
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=path.with_suffix(".png"),
        suffixes=(".png",),
    )
    figure, axis = plt.subplots(figsize=(8, 6))
    for wire in schematic.wires():
        axis.plot([wire.x1, wire.x2], [-wire.y1, -wire.y2], color="black", linewidth=1)
    for symbol in schematic.symbols():
        axis.scatter([symbol.x], [-symbol.y], color="tab:blue")
        axis.text(symbol.x, -symbol.y, symbol.reference(), fontsize=8)
    for flag in schematic.flags():
        axis.scatter([flag.x], [-flag.y], color="tab:red", marker="x")
        axis.text(flag.x, -flag.y, flag.name, fontsize=7, color="tab:red")
    axis.set_aspect("equal")
    axis.set_title(path.name)
    figure.tight_layout()
    buffer = BytesIO()
    figure.savefig(buffer, format="png", dpi=100)
    plt.close(figure)
    png = buffer.getvalue()
    destination.write_bytes(png)
    image = ImageResult(png=png, summary=f"Schematic preview of {path.name}.")
    return {"path": str(destination), **image.as_dict()}


def describe_edit_capability(*, workspace_root: Path) -> dict[str, object]:
    """Describe which edits the clean-room editor performs."""

    del workspace_root
    return {
        "format": "asc",
        "encoding": "latin-1",
        "grid": 16,
        "primitives": [
            "resistor",
            "capacitor",
            "inductor",
            "diode",
            "voltage_source",
            "current_source",
            "behavioral",
            "nmos",
            "pmos",
            "npn",
            "pnp",
            "opamp",
            "ground",
        ],
        "junctions": "implicit; add_junction splits a wire at a point",
    }


def describe_schematic_edit_support(*, workspace_root: Path) -> dict[str, object]:
    """Describe schematic edit support for clients."""

    return describe_edit_capability(workspace_root=workspace_root)


def read_component_symbol(*, workspace_root: Path, symbol_path: str) -> dict[str, object]:
    """Read an ``.asy`` symbol."""

    path = validate_existing_file(symbol_path, workspace_root=workspace_root, suffixes=(".asy",))
    symbol = load_asy(path)
    return {
        "path": str(path),
        "version": symbol.version,
        "symbol_type": symbol.symbol_type,
        "attributes": dict(symbol.attributes),
        "pins": [
            {"name": pin.name, "x": pin.x, "y": pin.y, "spice_order": pin.spice_order}
            for pin in symbol.pins
        ],
        "drawings": symbol.graphics,
    }


def export_symbol_to_asy(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    output_path: str,
) -> dict[str, object]:
    """Write a two-pin ``.asy`` named for a placed component."""

    _path, schematic, _previous = _load(workspace_root, schematic_path)
    symbol = schematic.find_symbol(reference)
    destination = resolve_output_path(
        output_path,
        workspace_root=workspace_root,
        default=workspace_root / f"{reference}.asy",
        suffixes=(".asy",),
    )
    asy = two_pin_box(
        prefix="X",
        value=symbol.attr("Value") or reference,
        description=f"Symbol exported for {reference} ({symbol.name}).",
    )
    save_asy(destination, asy)
    return {"path": str(destination), "reference": reference}


def add_component_from_asy(
    *,
    workspace_root: Path,
    schematic_path: str,
    asy_path: str,
    reference: str,
    value: str = "",
    x: int = 0,
    y: int = 0,
    rotation: str = "R0",
) -> dict[str, object]:
    """Place a symbol. Use the file name of an ``.asy`` in the workspace."""

    asy = validate_existing_file(asy_path, workspace_root=workspace_root, suffixes=(".asy",))
    loaded = load_asy(asy)
    chosen = value or loaded.attr("Value") or ""
    return add_library_component(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        symbol_name=asy.stem,
        reference=reference,
        value=chosen,
        x=x,
        y=y,
        rotation=rotation,
    )


def set_component_symbol_text(
    *, workspace_root: Path, asy_path: str, attribute: str, value: str
) -> dict[str, object]:
    """Set one ``.asy`` attribute."""

    path = validate_existing_file(asy_path, workspace_root=workspace_root, suffixes=(".asy",))
    symbol = load_asy(path)
    symbol.set_attr(attribute, value)
    save_asy(path, symbol)
    return {"path": str(path), "attribute": attribute, "value": value}


def set_component_symbol_pin(
    *,
    workspace_root: Path,
    asy_path: str,
    pin_name: str,
    x: int,
    y: int,
    spice_order: int,
) -> dict[str, object]:
    """Move or add a symbol pin."""

    path = validate_existing_file(asy_path, workspace_root=workspace_root, suffixes=(".asy",))
    symbol = load_asy(path)
    for pin in symbol.pins:
        if pin.name == pin_name:
            pin.x = x
            pin.y = y
            pin.spice_order = spice_order
            save_asy(path, symbol)
            return {"path": str(path), "pin": pin_name, "updated": True}
    symbol.pins.append(AsyPin(x, y, "NONE", 0, pin_name, spice_order))
    save_asy(path, symbol)
    return {"path": str(path), "pin": pin_name, "updated": False}


def add_component_symbol_drawing(
    *, workspace_root: Path, asy_path: str, kind: str, coords: str
) -> dict[str, object]:
    """Append a LINE, RECTANGLE, CIRCLE, or ARC to a symbol."""

    path = validate_existing_file(asy_path, workspace_root=workspace_root, suffixes=(".asy",))
    symbol = load_asy(path)
    keyword = kind.strip().upper()
    if keyword not in {"LINE", "RECTANGLE", "CIRCLE", "ARC"}:
        raise ValidationError("kind must be LINE, RECTANGLE, CIRCLE, or ARC.")
    symbol.graphics.append(f"{keyword} {coords.strip()}")
    save_asy(path, symbol)
    return {"path": str(path), "index": len(symbol.graphics) - 1}


def remove_component_symbol_drawing(
    *, workspace_root: Path, asy_path: str, index: int
) -> dict[str, object]:
    """Remove one symbol graphic by index."""

    path = validate_existing_file(asy_path, workspace_root=workspace_root, suffixes=(".asy",))
    symbol = load_asy(path)
    require_index(symbol, index)
    removed = symbol.graphics.pop(index)
    save_asy(path, symbol)
    return {"path": str(path), "removed": removed}


def normalize_component_text_rotation(
    *, workspace_root: Path, schematic_path: str
) -> dict[str, object]:
    """Reset attribute windows to left-justified text."""

    path, schematic, previous = _load(workspace_root, schematic_path)
    changed = 0
    for symbol in schematic.symbols():
        for window in symbol.windows:
            if window.justification != "Left":
                window.justification = "Left"
                changed += 1
    saved = _save(path, schematic, previous=previous)
    return {"changed_windows": changed, **saved}


def describe_schematic_layout_spec(
    *, workspace_root: Path, spec_name: str = "divider"
) -> dict[str, object]:
    """Describe a built-in layout spec."""

    del workspace_root
    summary = _LAYOUTS.get(spec_name, _LAYOUTS["divider"])
    return {"spec_name": spec_name, "summary": summary, "grid": 16}


def apply_schematic_layout_spec(
    *,
    workspace_root: Path,
    schematic_path: str,
    spec_name: str = "divider",
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Replace a schematic with a built-in layout."""

    path = resolve_output_path(
        schematic_path,
        workspace_root=workspace_root,
        default=workspace_root / f"{spec_name}.asc",
        suffixes=(".asc",),
    )
    schematic = build_named(spec_name, _version(settings))
    saved = _save(path, schematic, previous=_existing_findings(path))
    return {"path": str(path), "spec_name": spec_name, **saved}


def import_circuit_bundle(
    *, workspace_root: Path, bundle_path: str, destination_dir: str = ""
) -> dict[str, object]:
    """Unpack a zip of schematics into the workspace, or copy one ``.asc``."""

    source = validate_existing_file(bundle_path, workspace_root=workspace_root)
    destination = resolve_workspace_path(
        destination_dir or "imported", workspace_root=workspace_root
    )
    destination.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    if source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source) as archive:
            for info in archive.infolist():
                target = (destination / info.filename).resolve(strict=False)
                if (
                    destination.resolve(strict=False) not in target.parents
                    and target != destination
                ):
                    raise ValidationError(f"Zip entry escapes the destination: {info.filename}")
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(info))
                written.append(str(target))
    else:
        target = destination / source.name
        target.write_bytes(source.read_bytes())
        written.append(str(target))
    return {"destination": str(destination), "files": written}


def materialize_reference_circuit(
    *,
    workspace_root: Path,
    recipe_id: str,
    destination_path: str,
    settings: LTspiceSettings | None = None,
) -> dict[str, object]:
    """Write a built-in reference circuit."""

    return create_starter_schematic(
        workspace_root=workspace_root,
        schematic_path=destination_path,
        kind=recipe_id,
        settings=settings,
    )
