# In the name of God, the Most Gracious, the Most Merciful
"""LTspice symbols and behavioral scaffolds.

LTspice does not load user C++ DLLs, Verilog models, or socket devices.
These tools author ``.asy`` symbols, hierarchical blocks, and behavioral subcircuits.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ltspice_mcp.services._backends.asc_document import (
    Flag,
    IoPin,
    Schematic,
    load_schematic,
)
from ltspice_mcp.services._backends.asc_edit import (
    add_library_symbol,
    add_primitive,
    upsert_directive,
)
from ltspice_mcp.services._backends.asy_document import AsyPin, AsySymbol, save_asy, two_pin_box
from ltspice_mcp.services._backends.schematic_checks import schematic_findings
from ltspice_mcp.services._backends.schematic_commit import commit_schematic
from ltspice_mcp.services._shared.paths import resolve_output_path, validate_existing_file
from ltspice_mcp.services.schematic.operations import add_instruction

if TYPE_CHECKING:
    from pathlib import Path


def describe_mixed_signal_support(*, workspace_root: Path) -> dict[str, object]:
    """State the mixed-signal design tasks that LTspice can do. State the design tasks that LTspice cannot do."""

    del workspace_root
    return {
        "dll_devices": False,
        "verilog_devices": False,
        "socket_devices": False,
        "python_devices": False,
        "supported": ["asy_symbols", "hierarchical_blocks", "behavioral_sources"],
        "note": "LTspice has no C-block or DLL custom-device toolchain.",
    }


def describe_protocol_support(*, workspace_root: Path) -> dict[str, object]:
    """State that the I2C and SPI scaffolds here are behavioral circuits for instruction."""

    del workspace_root
    return {
        "i2c": "behavioral",
        "spi": "behavioral",
        "note": "Scaffolds are not bus transceivers and do not replace a digital model.",
    }


def create_asy_symbol(
    *,
    workspace_root: Path,
    output_path: str,
    prefix: str = "X",
    value: str = "block",
    description: str = "Custom two-pin cell",
) -> dict[str, object]:
    """Write a two-pin ``.asy`` symbol."""

    path = resolve_output_path(
        output_path,
        workspace_root=workspace_root,
        default=workspace_root / "block.asy",
        suffixes=(".asy",),
    )
    save_asy(path, two_pin_box(prefix=prefix, value=value, description=description))
    return {"path": str(path)}


def add_hierarchical_block(
    *,
    workspace_root: Path,
    schematic_path: str,
    block_name: str,
    reference: str,
    x: int = 200,
    y: int = 80,
) -> dict[str, object]:
    """Create a child sheet with In/Out pins and place it on the parent."""

    parent = validate_existing_file(
        schematic_path, workspace_root=workspace_root, suffixes=(".asc",)
    )
    child_path = parent.with_name(f"{block_name}.asc")
    symbol_path = parent.with_name(f"{block_name}.asy")
    child = Schematic()
    child.records.append(IoPin(80, 48, "In"))
    child.records.append(IoPin(240, 48, "Out"))
    child.records.append(Flag(80, 160, "0"))
    child_previous = schematic_findings(load_schematic(child_path)) if child_path.is_file() else ()
    commit_schematic(child_path, child, previous_findings=child_previous)
    symbol = AsySymbol()
    symbol.graphics.append("RECTANGLE Normal 0 0 96 64")
    symbol.attributes.append(("Prefix", "X"))
    symbol.attributes.append(("Value", block_name))
    symbol.attributes.append(("ModelFile", child_path.name))
    symbol.pins.append(AsyPin(0, 16, "NONE", 0, "In", 1))
    symbol.pins.append(AsyPin(96, 16, "NONE", 0, "Out", 2))
    save_asy(symbol_path, symbol)
    parent_sheet = load_schematic(parent)
    parent_previous = schematic_findings(parent_sheet)
    placed = add_library_symbol(
        parent_sheet,
        symbol_name=block_name,
        reference=reference,
        value=block_name,
        x=x,
        y=y,
        rotation="R0",
    )
    parent_symbol = parent_sheet.find_symbol(reference)
    parent_symbol.set_attr("ModelFile", child_path.name)
    placed.update(commit_schematic(parent, parent_sheet, previous_findings=parent_previous))
    placed["child"] = str(child_path)
    placed["symbol_path"] = str(symbol_path)
    return placed


def scaffold_behavioral_subcircuit(
    *,
    workspace_root: Path,
    output_path: str,
    expression: str = "V=V(A)*2",
) -> dict[str, object]:
    """Write a schematic whose only active device is a behavioral source."""

    path = resolve_output_path(
        output_path,
        workspace_root=workspace_root,
        default=workspace_root / "behavioral.asc",
        suffixes=(".asc",),
    )
    schematic = Schematic()
    add_primitive(
        schematic,
        kind="behavioral",
        reference="B1",
        value=expression,
        x=160,
        y=64,
        rotation="R0",
    )
    add_primitive(schematic, kind="ground", reference="", value="", x=160, y=176, rotation="R0")
    upsert_directive(schematic, ".op")
    previous = schematic_findings(load_schematic(path)) if path.is_file() else ()
    saved = commit_schematic(path, schematic, previous_findings=previous)
    return {"path": str(path), "expression": expression, **saved}


def scaffold_i2c_device(*, workspace_root: Path, output_path: str) -> dict[str, object]:
    """Write a behavioral sketch of an I2C open-drain pull-up, not a protocol engine."""

    created = scaffold_behavioral_subcircuit(
        workspace_root=workspace_root,
        output_path=output_path,
        expression="V=if(V(A)>2.5,5,0)",
    )
    add_instruction(
        workspace_root=workspace_root,
        schematic_path=str(created["path"]),
        text="; Behavioral I2C teaching scaffold. This is not an I2C transceiver.",
        x=80,
        y=320,
    )
    created["protocol"] = "i2c-behavioral"
    return created


def scaffold_spi_device(*, workspace_root: Path, output_path: str) -> dict[str, object]:
    """Write a behavioral sketch of a SPI data latch, not a protocol engine."""

    created = scaffold_behavioral_subcircuit(
        workspace_root=workspace_root,
        output_path=output_path,
        expression="V=V(A)",
    )
    add_instruction(
        workspace_root=workspace_root,
        schematic_path=str(created["path"]),
        text="; Behavioral SPI teaching scaffold. This is not a SPI transceiver.",
        x=80,
        y=320,
    )
    created["protocol"] = "spi-behavioral"
    return created
