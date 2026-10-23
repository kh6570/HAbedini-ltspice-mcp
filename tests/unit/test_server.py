# In the name of God, the Most Gracious, the Most Merciful
"""Catalog and capability tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ltspice_mcp.core.exceptions import UnsupportedError
from ltspice_mcp.infra.config import build_settings
from ltspice_mcp.mcp.server import create_server
from ltspice_mcp.services.live_gui.operations import send_live_gui_session_command

if TYPE_CHECKING:
    from pathlib import Path


def test_describe_lists_ltspice_tools(tmp_path: Path) -> None:
    settings = build_settings(workspace_root=tmp_path, log_level="error")
    server = create_server(settings)
    summary = server.summary()
    assert summary["engine"] == "ltspice"
    names = summary["registered_tools"]
    assert isinstance(names, list)
    assert "run_simulation" in names
    assert "create_schematic" in names
    assert "read_waveform" in names
    assert "describe_server_capabilities" in names
    assert "add_dll_block" not in names
    described = server.invoke_tool("describe_server_capabilities")
    features = described["features"]
    assert isinstance(features, dict)
    assert features["dll_devices"] is False
    hidden = described["hidden_groups"]
    assert isinstance(hidden, list)
    groups = {item["group"] for item in hidden if isinstance(item, dict)}
    assert {"batch", "remote", "live_gui", "topology_ingest"} <= groups
    enable = described["extended_profiles"]
    assert isinstance(enable, dict)
    assert "LTSPICE_ACTIVE_PROFILES=default,extended" in str(enable["enable"])
    assert "no message bridge" not in str(described).lower()


def test_gui_command_is_unsupported(tmp_path: Path) -> None:
    schematic = tmp_path / "empty.asc"
    schematic.write_text("Version 4\nSHEET 1 880 680\n", encoding="latin-1")
    with pytest.raises(UnsupportedError):
        send_live_gui_session_command(
            workspace_root=tmp_path, schematic_path="empty.asc", command="run"
        )
