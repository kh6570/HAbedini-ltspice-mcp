# In the name of God, the Most Gracious, the Most Merciful
"""Workflow notes stay short routers; procedures live in skill references."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from mcp_app_core.skills import load_skill, load_skill_reference

from ltspice_mcp.services.instructions.operations import (
    list_workflow_instructions,
    read_workflow_instruction,
)

_RUN_STEP = "Use `read_waveform` when you need the trace, and stay inside the 2000 point budget."
_DEBUG_STEP = "A missing `FLAG ... 0` is the usual first problem."


def _skill_dir(group: str, name: str) -> Path:
    return Path(str(files("ltspice_mcp.data.skills") / group / name))


def test_workflow_instructions_return_routers_without_reference_bodies(tmp_path: Path) -> None:
    listed = list_workflow_instructions(workspace_root=tmp_path)
    assert listed["instructions"] == ["debug-convergence", "run-and-measure"]

    run = read_workflow_instruction(workspace_root=tmp_path, name="run-and-measure")
    run_text = str(run["text"])
    assert "ltspice-run-and-measure" in run_text
    assert _RUN_STEP not in run_text
    run_reference = load_skill_reference(
        _skill_dir("ltspice-procedures", "ltspice-run-and-measure"),
        "workflow.md",
    )
    assert _RUN_STEP in run_reference

    debug = read_workflow_instruction(workspace_root=tmp_path, name="debug-convergence")
    debug_text = str(debug["text"])
    assert "ltspice-debug-convergence" in debug_text
    assert _DEBUG_STEP not in debug_text
    debug_reference = load_skill_reference(
        _skill_dir("ltspice-procedures", "ltspice-debug-convergence"),
        "workflow.md",
    )
    assert _DEBUG_STEP in debug_reference


def test_default_skill_group_is_orientation_only() -> None:
    root = Path(str(files("ltspice_mcp.data.skills")))
    core_names = {path.name for path in (root / "ltspice-core").iterdir() if path.is_dir()}
    procedure_names = {
        path.name for path in (root / "ltspice-procedures").iterdir() if path.is_dir()
    }
    assert core_names == {"ltspice-getting-started"}
    assert procedure_names == {"ltspice-debug-convergence", "ltspice-run-and-measure"}
    loaded = load_skill(_skill_dir("ltspice-core", "ltspice-getting-started"))
    assert loaded.manifest.reference_files == ("batch-contract.md",)
    assert _RUN_STEP not in loaded.body
    assert _DEBUG_STEP not in loaded.body
