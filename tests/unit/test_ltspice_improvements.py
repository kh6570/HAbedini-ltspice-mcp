# In the name of God, the Most Gracious, the Most Merciful
"""Profiles, hash commits, checks, images, fresh logs, and window sync."""

from __future__ import annotations

import asyncio
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import pytest
from mcp_app_core.commit import commit_file as real_commit
from mcp_app_core.commit import file_content_sha256

from ltspice_mcp.adapters.bridge_client import (
    BridgeToolsChangedError,
    prepare_window,
    run_window_guard,
    texts_match,
    use_bridge_opener,
    user_gui_pid,
)
from ltspice_mcp.adapters.cli.ltspice_v1 import build_batch_command, classify_simulation_log
from ltspice_mcp.adapters.probe import (
    ProbeResult,
    bridge_executable_for,
    probe_ltspice,
    version_at_least,
)
from ltspice_mcp.core.exceptions import ContentConflictError, SimulationError, ValidationError
from ltspice_mcp.infra.call_context import bind_content_hash, bind_settings
from ltspice_mcp.infra.config import LTspiceSettings, build_settings
from ltspice_mcp.mcp.server import create_server
from ltspice_mcp.services._backends.log_parse import operating_point_report
from ltspice_mcp.services._backends.simulation_runner import require_fresh_log
from ltspice_mcp.services._backends.waveform_math import apply_budget
from ltspice_mcp.services.schematic.operations import (
    add_component,
    apply_schematic_layout_spec,
    check_netlist,
    check_schematic,
    create_schematic,
    render_schematic_image,
)
from ltspice_mcp.services.waveform.operations import plot_waveforms

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class _FakeBridge:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.names = {
            "status",
            "attach",
            "list_open_designs",
            "get_design_content",
            "set_design_content",
        }
        self.status_body: dict[str, object] = {
            "instances": [{"mode": "gui-attached", "pid": 7, "autoStarted": False}]
        }
        self.open_paths: list[str] = []
        self.buffer = ""
        self.pushed: tuple[str, str] | None = None

    def tool_names(self) -> set[str]:
        return set(self.names)

    async def status(self) -> dict[str, object]:
        self.calls.append("status")
        return self.status_body

    async def attach(self, pid: int) -> None:
        self.calls.append(f"attach:{pid}")

    async def list_open_designs(self) -> list[str]:
        self.calls.append("list")
        return list(self.open_paths)

    async def read_design(self, path: str) -> str:
        self.calls.append("read")
        del path
        return self.buffer

    async def replace_design(self, path: str, text: str) -> None:
        self.calls.append("replace")
        self.pushed = (path, text)


def test_default_profile_hides_extended_groups(tmp_path: Path) -> None:
    settings = build_settings(workspace_root=tmp_path, log_level="error")
    server = create_server(settings)
    names = server.summary()["registered_tools"]
    assert isinstance(names, list)
    assert "create_schematic" in names
    assert "submit_batch" not in names
    assert "submit_remote_simulation" not in names
    assert "open_schematic_in_gui" not in names
    assert "ingest_topology_contribution" not in names
    described = server.invoke_tool("describe_server_capabilities")
    hidden = described["hidden_groups"]
    assert isinstance(hidden, list)
    groups = {item["group"] for item in hidden if isinstance(item, dict)}
    assert groups == {"batch", "remote", "live_gui", "topology_ingest"}

    extended = create_server(
        build_settings(
            workspace_root=tmp_path,
            log_level="error",
            active_profiles="default,extended",
        )
    )
    extended_names = extended.summary()["registered_tools"]
    assert isinstance(extended_names, list)
    assert "submit_batch" in extended_names
    assert "ingest_topology_contribution" in extended_names


def test_hash_mismatch_writes_nothing(tmp_path: Path) -> None:
    created = create_schematic(workspace_root=tmp_path, schematic_path="empty.asc")
    path = Path(str(created["path"]))
    original = path.read_bytes()
    with bind_content_hash("0" * 64, path), pytest.raises(ContentConflictError):
        add_component(
            workspace_root=tmp_path,
            schematic_path="empty.asc",
            kind="resistor",
            reference="R1",
            value="1k",
        )
    assert path.read_bytes() == original


def test_layout_commits_once_and_splits_findings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "layout.asc"
    path.write_text("Version 4\nSHEET 1 880 680\n", encoding="latin-1")
    calls: list[int] = []

    def wrapped(target: Path, *, expected_hash: str, content: bytes) -> str:
        calls.append(1)
        return real_commit(target, expected_hash=expected_hash, content=content)

    monkeypatch.setattr(
        "ltspice_mcp.services._backends.schematic_commit.commit_file",
        wrapped,
    )
    with bind_content_hash(file_content_sha256(path), path):
        result = apply_schematic_layout_spec(
            workspace_root=tmp_path,
            schematic_path="layout.asc",
            spec_name="divider",
        )
    assert calls == [1]
    findings = result["findings"]
    assert isinstance(findings, dict)
    assert "previous" in findings
    assert "introduced" in findings


def test_check_findings_include_location_and_fixable(tmp_path: Path) -> None:
    create_schematic(workspace_root=tmp_path, schematic_path="empty.asc")
    checked = check_schematic(workspace_root=tmp_path, schematic_path="empty.asc")
    findings = checked["findings"]
    assert isinstance(findings, list)
    assert findings
    for finding in findings:
        assert isinstance(finding, dict)
        assert isinstance(finding["fixable"], bool)
        assert "location" in finding
    netlist = tmp_path / "bare.net"
    netlist.write_text("R1 in out 1k\nR1 in 0 2k\n.end\n", encoding="utf-8")
    net_checked = check_netlist(workspace_root=tmp_path, netlist_path="bare.net")
    net_findings = net_checked["findings"]
    assert isinstance(net_findings, list)
    codes = {item["code"] for item in net_findings if isinstance(item, dict)}
    assert "duplicate_reference" in codes
    assert "missing_analysis" in codes
    duplicate = next(
        item
        for item in net_findings
        if isinstance(item, dict) and item["code"] == "duplicate_reference"
    )
    assert duplicate["fixable"] is True
    assert str(duplicate["location"]).startswith("line ")


def test_minmax_keeps_a_spike(tmp_path: Path) -> None:
    del tmp_path
    count = 100
    x_values = np.arange(count, dtype=np.float64)
    y_values = np.zeros(count, dtype=np.complex128)
    y_values[50] = 10
    _xs, real, _imag, downsampled = apply_budget(x_values, y_values, max_points=8)
    assert downsampled is True
    assert max(real) == 10.0


def test_render_returns_png(tmp_path: Path) -> None:
    create_schematic(workspace_root=tmp_path, schematic_path="empty.asc")
    rendered = render_schematic_image(workspace_root=tmp_path, schematic_path="empty.asc")
    assert rendered["media_type"] == "image/png"
    assert Path(str(rendered["path"])).is_file()
    encoded = rendered["png_base64"]
    assert isinstance(encoded, str)
    assert encoded.startswith("iVBOR")


def test_plot_returns_png(tmp_path: Path) -> None:
    raw = tmp_path / "demo.raw"
    raw.write_text(
        "\n".join(
            [
                "Title: test",
                "Plotname: Transient Analysis",
                "Flags: real",
                "No. Variables: 2",
                "No. Points: 4",
                "Variables:",
                "\t0\ttime\ttime",
                "\t1\tV(out)\tvoltage",
                "Values:",
                "0\t0",
                "\t0",
                "1\t0.001",
                "\t5",
                "2\t0.002",
                "\t1",
                "3\t0.003",
                "\t5",
            ]
        ),
        encoding="latin-1",
    )
    plotted = plot_waveforms(workspace_root=tmp_path, raw_path="demo.raw", signals="V(out)")
    assert plotted["media_type"] == "image/png"
    assert Path(str(plotted["path"])).read_bytes().startswith(b"\x89PNG")


def test_stale_log_is_rejected(tmp_path: Path) -> None:
    log = tmp_path / "demo.log"
    log.write_text("Total elapsed time: 0.1 seconds.\n", encoding="utf-8")
    with pytest.raises(SimulationError):
        require_fresh_log(log, started_at=time.time() + 60)
    fresh = time.time()
    stamped = time.time() + 2
    os.utime(log, (stamped, stamped))
    text = require_fresh_log(log, started_at=fresh)
    assert "Total elapsed time" in text
    with pytest.raises(SimulationError):
        classify_simulation_log("Circuit: demo\n", return_code=0)


def test_op_raw_is_added_to_log_points(tmp_path: Path) -> None:
    log = tmp_path / "demo.log"
    log.write_text(
        "Operating point\nV(out): 1.5 voltage\n\nTotal elapsed time: 0.1 seconds.\n",
        encoding="utf-8",
    )
    (tmp_path / "demo.op.raw").write_text(
        "\n".join(
            [
                "Title: op",
                "Plotname: Operating Point",
                "Flags: real",
                "No. Variables: 2",
                "No. Points: 1",
                "Variables:",
                "\t0\ttime\ttime",
                "\t1\tV(in)\tvoltage",
                "Values:",
                "0\t0",
                "\t3.25",
            ]
        ),
        encoding="latin-1",
    )
    report = operating_point_report(log)
    points = report["points"]
    assert isinstance(points, list)
    sources = {str(item["source"]) for item in points if isinstance(item, dict)}
    names = {str(item["name"]) for item in points if isinstance(item, dict)}
    assert sources == {"log", "op.raw"}
    assert "V(in)" in names


def test_version_and_bridge_sibling(tmp_path: Path) -> None:
    exe = tmp_path / "LTspice.exe"
    bridge = tmp_path / "ltspice-mcp-bridge.exe"
    exe.write_bytes(b"exe")
    bridge.write_bytes(b"bridge")
    assert bridge_executable_for(exe) == bridge
    assert version_at_least("26.1.1.0", 26, 1) is True
    assert version_at_least("17.0.37.0", 26, 1) is False
    installed = Path(r"C:\Program Files\ADI\LTspice\LTspice.exe")
    if installed.is_file():
        probed = probe_ltspice(LTspiceSettings(exe=installed, workspace_root=tmp_path))
        assert probed.bridge_exists is True
        assert probed.message_bridge is True


def test_batch_refuses_schematic() -> None:
    with pytest.raises(ValidationError):
        build_batch_command(Path("LTspice.exe"), Path("divider.asc"))


def test_window_sync_does_not_start_hidden_ltspice(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "open.asc"
    path.write_text("Version 4\nSHEET 1 880 680\n", encoding="latin-1")
    bridge = tmp_path / "ltspice-mcp-bridge.exe"
    bridge.write_bytes(b"bridge")
    fake = _FakeBridge()
    fake.open_paths = [str(path)]
    fake.buffer = "edited in the window"

    @asynccontextmanager
    async def opener(executable: Path) -> AsyncIterator[_FakeBridge]:
        assert executable == bridge
        yield fake

    monkeypatch.setattr(
        "ltspice_mcp.adapters.bridge_client.probe_ltspice",
        lambda _settings: ProbeResult(
            configured=True,
            executable=tmp_path / "LTspice.exe",
            exists=True,
            source="configured",
            version="26.1.1.0",
            bridge_executable=bridge,
            bridge_exists=True,
            message_bridge=True,
        ),
    )
    settings = LTspiceSettings(workspace_root=tmp_path, window_sync=True, exe=bridge)

    def write() -> str:
        raise AssertionError("A dirty window must be left unchanged.")

    with (
        bind_settings(settings),
        use_bridge_opener(opener),
        pytest.raises(ValidationError, match="Save the schematic"),
    ):
        run_window_guard(path, path.read_text(encoding="latin-1"), "next", write)
    assert path.read_text(encoding="latin-1").startswith("Version 4")
    assert "start_headless" not in fake.calls
    assert "replace" not in fake.calls

    fake.buffer = path.read_text(encoding="latin-1")
    fake.calls.clear()
    written: list[str] = []

    def save() -> str:
        written.append("saved")
        path.write_text("Version 4\nSHEET 1 880 680\nWIRE 0 0 16 0\n", encoding="latin-1")
        return "abc"

    with bind_settings(settings), use_bridge_opener(opener):
        digest, sync = run_window_guard(
            path,
            "Version 4\nSHEET 1 880 680\n",
            "Version 4\nSHEET 1 880 680\nWIRE 0 0 16 0\n",
            save,
        )
    assert digest == "abc"
    assert written == ["saved"]
    assert isinstance(sync, dict)
    assert sync["pushed"] is True
    assert fake.pushed is not None
    assert fake.calls.count("replace") == 1
    assert "start_headless" not in fake.calls

    fake.status_body = {"instances": [{"mode": "headless", "pid": 9, "autoStarted": True}]}
    fake.calls.clear()
    fake.pushed = None

    def save_again() -> str:
        return "def"

    with bind_settings(settings), use_bridge_opener(opener):
        _digest, sync = run_window_guard(path, "disk", "next", save_again)
    assert isinstance(sync, dict)
    assert sync["pushed"] is False
    assert not any(call.startswith("attach") for call in fake.calls)


def test_user_gui_pid_ignores_headless() -> None:
    assert user_gui_pid({"instances": [{"mode": "headless", "pid": 3}]}) is None
    assert user_gui_pid({"instances": [{"mode": "gui-attached", "pid": 4}]}) == 4
    assert texts_match("A\r\nB\n", "A\nB") is True


def test_changed_bridge_tools_fall_back(tmp_path: Path) -> None:
    fake = _FakeBridge()
    fake.names = {"status"}

    async def _prepare() -> None:
        with pytest.raises(BridgeToolsChangedError):
            await prepare_window(fake, tmp_path / "a.asc", "disk")

    asyncio.run(_prepare())


def test_setup_script_uses_ltspice_mcp_name() -> None:
    script = Path(__file__).resolve().parents[2] / "scripts" / "setup_mcp.ps1"
    text = script.read_text(encoding="utf-8")
    assert '"ltspice-mcp"' in text
    assert '"ltspice"' not in text
