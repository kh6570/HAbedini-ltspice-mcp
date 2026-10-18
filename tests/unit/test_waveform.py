# In the name of God, the Most Gracious, the Most Merciful
"""Waveform and log parsing tests that do not launch LTspice."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ltspice_mcp.adapters.cli.ltspice_v1 import classify_simulation_log
from ltspice_mcp.services.waveform.operations import read_measures, read_waveform

if TYPE_CHECKING:
    from pathlib import Path

_RAW = """Title: test
Plotname: Transient Analysis
Flags: real
No. Variables: 2
No. Points: 4
Variables:
\t0\ttime\ttime
\t1\tV(out)\tvoltage
Values:
0\t0
\t0
1\t0.001
\t5
2\t0.002
\t5
3\t0.003
\t5
"""

_LOG = """Circuit: divider
.step param run=1

Measurement: vout
  step\tAVG(v(out))\tFROM\tTO
     1\t5\t0\t0.001

Date: Sun Oct 18 2026
Total elapsed time: 0.012 seconds.
"""


def test_ascii_raw_and_meas_log(tmp_path: Path) -> None:
    raw_path = tmp_path / "demo.raw"
    log_path = tmp_path / "demo.log"
    raw_path.write_text(_RAW, encoding="latin-1")
    log_path.write_text(_LOG, encoding="latin-1")
    waveform = read_waveform(workspace_root=tmp_path, raw_path="demo.raw", signal="V(out)")
    real = waveform["real"]
    assert isinstance(real, list)
    assert real[-1] == 5.0
    measures = read_measures(workspace_root=tmp_path, log_path="demo.log")
    assert measures["measures"]
    assert measures["measures"][0]["name"] == "vout"


def test_log_classifier_accepts_success() -> None:
    classify_simulation_log(_LOG, return_code=0)
