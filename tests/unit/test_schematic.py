# In the name of God, the Most Gracious, the Most Merciful
"""Schematic editor and clean-room netlist tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from ltspice_mcp.core.exceptions import SandboxViolationError
from ltspice_mcp.services._backends.asc_document import load_schematic, parse_schematic
from ltspice_mcp.services._backends.starters import build_divider
from ltspice_mcp.services._shared.paths import resolve_workspace_path
from ltspice_mcp.services.schematic.operations import (
    check_schematic,
    create_schematic,
    create_starter_schematic,
)
from ltspice_mcp.services.simulation.operations import generate_netlist


def test_round_trip_preserves_version_and_symbols(tmp_path: Path) -> None:
    created = create_starter_schematic(
        workspace_root=tmp_path, schematic_path="divider.asc", kind="divider"
    )
    schematic = load_schematic(Path(str(created["path"])))
    assert schematic.version == "Version 4"
    names = {symbol.reference() for symbol in schematic.symbols()}
    assert names == {"V1", "R1", "R2"}
    again = parse_schematic(schematic.emit())
    assert {symbol.reference() for symbol in again.symbols()} == names


def test_clean_room_divider_netlist_connects_output(tmp_path: Path) -> None:
    create_starter_schematic(workspace_root=tmp_path, schematic_path="divider.asc")
    result = generate_netlist(
        workspace_root=tmp_path,
        source_path="divider.asc",
        use_simulator=False,
    )
    text = str(result["text"])
    assert "R1" in text
    assert "R2" in text
    assert "V1" in text
    assert "out" in text
    assert ".tran 1m" in text
    checked = check_schematic(workspace_root=tmp_path, schematic_path="divider.asc")
    assert checked["ok"] is True
    assert checked["findings"] == []
    assert isinstance(checked["content_hash"], str)
    assert len(str(checked["content_hash"])) == 64


def test_blank_schematic_and_sandbox(tmp_path: Path) -> None:
    created = create_schematic(workspace_root=tmp_path, schematic_path="empty.asc")
    text = Path(str(created["path"])).read_text(encoding="latin-1")
    assert text.startswith("Version 4")
    with pytest.raises(SandboxViolationError):
        resolve_workspace_path(tmp_path.parent / "outside-workspace.txt", workspace_root=tmp_path)


def test_micro_sign_round_trip() -> None:
    schematic = build_divider()
    schematic.symbols()[1].set_attr("Value", "1k\u00b5")
    parsed = parse_schematic(schematic.emit())
    assert parsed.symbols()[1].attr("Value") == "1k\u00b5"
