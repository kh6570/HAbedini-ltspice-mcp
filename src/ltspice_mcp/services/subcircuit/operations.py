# In the name of God, the Most Gracious, the Most Merciful
"""Subcircuit and hierarchical-sheet use cases."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ltspice_mcp.core.exceptions import ValidationError
from ltspice_mcp.services._backends.asc_document import IoPin, load_schematic, save_schematic
from ltspice_mcp.services._backends.asc_edit import set_component_parameters, set_component_value
from ltspice_mcp.services._shared.paths import resolve_workspace_path, validate_existing_file

if TYPE_CHECKING:
    from pathlib import Path

_SUBCKT = re.compile(r"^\.subckt\s+(\S+)", re.IGNORECASE)
_ENDS = re.compile(r"^\.ends\b", re.IGNORECASE)


def _read(path: Path) -> str:
    return path.read_text(encoding="latin-1", errors="replace")


def list_subcircuits(*, workspace_root: Path, source_path: str) -> dict[str, object]:
    """List ``.subckt`` blocks and hierarchical symbols."""

    path = validate_existing_file(
        source_path,
        workspace_root=workspace_root,
        suffixes=(".asc", ".lib", ".cir", ".net", ".sub"),
    )
    names: list[str] = []
    if path.suffix.lower() == ".asc":
        schematic = load_schematic(path)
        names.extend(
            symbol.reference()
            for symbol in schematic.symbols()
            if (symbol.attr("ModelFile") or symbol.name.lower().endswith(".asc"))
        )
        text = "\n".join(item.body() for item in schematic.texts())
    else:
        text = _read(path)
    names.extend(match.group(1) for match in _SUBCKT.finditer(text))
    return {"path": str(path), "subcircuits": names}


def read_subcircuit(*, workspace_root: Path, source_path: str, name: str) -> dict[str, object]:
    """Return one ``.subckt`` body or a hierarchical sheet."""

    path = validate_existing_file(
        source_path,
        workspace_root=workspace_root,
        suffixes=(".asc", ".lib", ".cir", ".net", ".sub"),
    )
    if path.suffix.lower() == ".asc":
        schematic = load_schematic(path)
        for symbol in schematic.symbols():
            model_file = symbol.attr("ModelFile")
            if symbol.reference() == name and model_file:
                child = resolve_workspace_path(model_file, workspace_root=path.parent)
                if child.is_file():
                    loaded = load_schematic(child)
                    return {
                        "name": name,
                        "path": str(child),
                        "iopins": [
                            {"x": pin.x, "y": pin.y, "direction": pin.direction}
                            for pin in loaded.records
                            if isinstance(pin, IoPin)
                        ],
                    }
        text = "\n".join(item.body() for item in schematic.texts())
    else:
        text = _read(path)
    lines = text.splitlines()
    body: list[str] = []
    capture = False
    for line in lines:
        if _SUBCKT.match(line.strip()) and line.split()[1] == name:
            capture = True
        if capture:
            body.append(line)
            if _ENDS.match(line.strip()):
                break
    if not body:
        raise ValidationError(f"Subcircuit {name!r} was not found.")
    return {"name": name, "text": "\n".join(body)}


def set_subcircuit_component_value(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    value: str,
) -> dict[str, object]:
    """Set a value on a component inside a schematic subcircuit file."""

    path = validate_existing_file(schematic_path, workspace_root=workspace_root, suffixes=(".asc",))
    schematic = load_schematic(path)
    result = set_component_value(schematic, reference, value)
    save_schematic(path, schematic)
    return result


def set_subcircuit_component_parameters(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    spice_line: str,
    spice_line2: str = "",
) -> dict[str, object]:
    """Set SpiceLine on a component inside a schematic subcircuit file."""

    path = validate_existing_file(schematic_path, workspace_root=workspace_root, suffixes=(".asc",))
    schematic = load_schematic(path)
    result = set_component_parameters(schematic, reference, spice_line, spice_line2)
    save_schematic(path, schematic)
    return result
