# In the name of God, the Most Gracious, the Most Merciful
"""Real LTspice XVII simulation of the bundled divider."""

from __future__ import annotations

from pathlib import Path

import pytest

from ltspice_mcp.infra.config import build_settings
from ltspice_mcp.services.schematic.operations import create_starter_schematic
from ltspice_mcp.services.simulation.operations import run_simulation_service
from ltspice_mcp.services.waveform.operations import read_measures, read_waveform

pytestmark = pytest.mark.integration


def test_divider_half_voltage(tmp_path: Path) -> None:
    settings = build_settings(workspace_root=tmp_path, log_level="error")
    create_starter_schematic(
        workspace_root=tmp_path,
        schematic_path="divider.asc",
        kind="divider",
        settings=settings,
    )
    result = run_simulation_service(
        workspace_root=tmp_path,
        source_path="divider.asc",
        settings=settings,
        ascii_raw=True,
        timeout_s=60,
    )
    assert Path(str(result["log_path"])).is_file()
    assert Path(str(result["raw_path"])).is_file()
    waveform = read_waveform(
        workspace_root=tmp_path,
        raw_path=str(result["raw_path"]),
        signal="V(out)",
    )
    samples = waveform["real"]
    assert isinstance(samples, list)
    assert samples
    average = sum(float(value) for value in samples) / len(samples)
    assert abs(average - 5.0) < 0.25
    measures = read_measures(workspace_root=tmp_path, log_path=str(result["log_path"]))
    assert measures["measures"]
