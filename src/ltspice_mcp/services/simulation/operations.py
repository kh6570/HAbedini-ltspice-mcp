# In the name of God, the Most Gracious, the Most Merciful
"""Simulation use cases."""

from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

from ltspice_mcp.adapters.probe import library_root, probe_ltspice
from ltspice_mcp.core.exceptions import (
    ArtifactMissingError,
    LTspiceError,
    ValidationError,
)
from ltspice_mcp.infra.config import LTspiceSettings
from ltspice_mcp.infra.subprocess_runner import _kill_process_tree
from ltspice_mcp.services._backends.asc_document import Schematic, load_schematic
from ltspice_mcp.services._backends.asc_edit import (
    set_component_value,
    set_element_model,
    upsert_directive,
)
from ltspice_mcp.services._backends.netlist_clean import render_clean_room_netlist
from ltspice_mcp.services._backends.schematic_checks import schematic_findings
from ltspice_mcp.services._backends.schematic_commit import commit_schematic
from ltspice_mcp.services._backends.simulation_runner import run_netlist, run_simulation
from ltspice_mcp.services._backends.waveform_math import find_signal, load_primary, split_steps
from ltspice_mcp.services._internals.active_runs import cancel_run as lookup_run
from ltspice_mcp.services._internals.active_runs import pop_run
from ltspice_mcp.services._shared.paths import (
    resolve_output_path,
    resolve_workspace_path,
    validate_existing_file,
)

if TYPE_CHECKING:
    from pathlib import Path

    from mcp_app_core.checks import CheckFinding

_SOURCE_SUFFIXES = (".asc", ".net", ".cir")


def _source(workspace_root: Path, source_path: str) -> Path:
    return validate_existing_file(
        source_path, workspace_root=workspace_root, suffixes=_SOURCE_SUFFIXES
    )


def _schematic(
    workspace_root: Path, schematic_path: str
) -> tuple[Path, Schematic, tuple[CheckFinding, ...]]:
    path = validate_existing_file(schematic_path, workspace_root=workspace_root, suffixes=(".asc",))
    schematic = load_schematic(path)
    return path, schematic, schematic_findings(schematic)


def _store(
    path: Path,
    schematic: Schematic,
    previous: tuple[CheckFinding, ...],
) -> dict[str, object]:
    saved = commit_schematic(path, schematic, previous_findings=previous)
    saved["path"] = str(path)
    return saved


def _edit_directive(
    workspace_root: Path,
    schematic_path: str,
    text: str,
    *,
    replace_command: str | None = None,
    comment_other_analyses: bool = False,
) -> dict[str, object]:
    path, schematic, previous = _schematic(workspace_root, schematic_path)
    result = upsert_directive(
        schematic,
        text,
        replace_command=replace_command,
        comment_other_analyses=comment_other_analyses,
    )
    result.update(_store(path, schematic, previous))
    return result


def generate_netlist(
    *,
    workspace_root: Path,
    source_path: str,
    output_path: str = "",
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
    use_simulator: bool = True,
) -> dict[str, object]:
    """Write a netlist with LTspice ``-netlist``, or the clean-room renderer."""

    source = _source(workspace_root, source_path)
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_suffix(".net"),
        suffixes=(".net", ".cir"),
    )
    if source.suffix.lower() in {".net", ".cir"}:
        if source.resolve() != destination.resolve():
            shutil.copyfile(source, destination)
        text = destination.read_text(encoding="latin-1", errors="replace")
        return {"engine": "copy", "netlist_path": str(destination), "text": text}
    effective = settings or LTspiceSettings(workspace_root=workspace_root)
    if use_simulator:
        try:
            produced = run_netlist(source, settings=effective, executable=ltspice_executable)
        except LTspiceError:
            produced = None
        if produced is not None:
            if produced.resolve() != destination.resolve():
                shutil.copyfile(produced, destination)
            text = destination.read_text(encoding="utf-8", errors="replace")
            return {"engine": "ltspice", "netlist_path": str(destination), "text": text}
    schematic = load_schematic(source)
    text = render_clean_room_netlist(schematic)
    destination.write_text(text, encoding="utf-8")
    return {"engine": "clean-room", "netlist_path": str(destination), "text": text}


def save_netlist_copy(
    *, workspace_root: Path, source_path: str, destination_path: str
) -> dict[str, object]:
    """Copy a netlist inside the workspace."""

    source = validate_existing_file(
        source_path, workspace_root=workspace_root, suffixes=(".net", ".cir", ".asc")
    )
    destination = resolve_output_path(
        destination_path,
        workspace_root=workspace_root,
        default=source.with_name(source.stem + "-copy.net"),
        suffixes=(".net", ".cir"),
    )
    if source.suffix.lower() == ".asc":
        destination.write_text(render_clean_room_netlist(load_schematic(source)), encoding="utf-8")
    else:
        shutil.copyfile(source, destination)
    return {"path": str(destination)}


def list_includes(*, workspace_root: Path, source_path: str) -> dict[str, object]:
    """List ``.lib`` and ``.include`` directives."""

    source = _source(workspace_root, source_path)
    text = source.read_text(encoding="latin-1", errors="replace")
    if source.suffix.lower() == ".asc":
        text = "\n".join(item.body() for item in load_schematic(source).texts())
    includes = [
        line.strip()
        for line in text.splitlines()
        if line.strip().lower().startswith((".lib", ".include"))
    ]
    return {"includes": includes}


def resolve_model_libraries(
    *,
    workspace_root: Path,
    model_name: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Search the workspace and the LTspice lib tree for a model name."""

    needle = model_name.lower()
    roots = [workspace_root]
    exe = ltspice_executable
    if exe is None and settings is not None:
        exe = probe_ltspice(settings).executable
    lib = library_root(exe)
    if lib is not None:
        roots.append(lib)
    hits: list[str] = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() not in {".lib", ".sub", ".cir", ".mod"}:
                continue
            try:
                text = path.read_text(encoding="latin-1", errors="ignore")
            except OSError:
                continue
            if needle in text.lower():
                hits.append(str(path))
            if len(hits) >= 20:
                break
    return {"model_name": model_name, "matches": hits}


def add_library_include(
    *, workspace_root: Path, schematic_path: str, library_path: str
) -> dict[str, object]:
    """Add a ``.lib`` directive."""

    library = resolve_workspace_path(library_path, workspace_root=workspace_root)
    return _edit_directive(workspace_root, schematic_path, f".lib {library.name}")


def add_model(*, workspace_root: Path, schematic_path: str, model_text: str) -> dict[str, object]:
    """Add a ``.model`` directive."""

    return _edit_directive(workspace_root, schematic_path, model_text, replace_command="")


def prepare_transient(
    *,
    workspace_root: Path,
    schematic_path: str,
    t_stop: str,
    t_step: str = "",
    t_start: str = "",
    max_step: str = "",
) -> dict[str, object]:
    """Insert a ``.tran`` directive."""

    parts = [".tran"]
    if t_step:
        parts.append(t_step)
    parts.append(t_stop)
    if t_start:
        parts.append(t_start)
    if max_step:
        parts.append(max_step)
    return _edit_directive(
        workspace_root,
        schematic_path,
        " ".join(parts),
        comment_other_analyses=True,
    )


def prepare_ac(
    *,
    workspace_root: Path,
    schematic_path: str,
    sweep: str = "dec",
    points: int = 100,
    f_start: str = "1",
    f_end: str = "1Meg",
) -> dict[str, object]:
    """Insert a ``.ac`` directive."""

    return _edit_directive(
        workspace_root,
        schematic_path,
        f".ac {sweep} {points} {f_start} {f_end}",
        comment_other_analyses=True,
    )


def prepare_dc_sweep(
    *,
    workspace_root: Path,
    schematic_path: str,
    source: str,
    start: str,
    stop: str,
    step: str,
) -> dict[str, object]:
    """Insert a ``.dc`` directive."""

    return _edit_directive(
        workspace_root,
        schematic_path,
        f".dc {source} {start} {stop} {step}",
        comment_other_analyses=True,
    )


def prepare_op(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Insert a ``.op`` directive."""

    return _edit_directive(workspace_root, schematic_path, ".op", comment_other_analyses=True)


def prepare_noise(
    *,
    workspace_root: Path,
    schematic_path: str,
    output: str,
    source: str,
    sweep: str = "dec",
    points: int = 100,
    f_start: str = "1",
    f_end: str = "1Meg",
) -> dict[str, object]:
    """Insert a ``.noise`` directive."""

    text = f".noise {output} {source} {sweep} {points} {f_start} {f_end}"
    return _edit_directive(workspace_root, schematic_path, text, comment_other_analyses=True)


def prepare_transfer_function(
    *, workspace_root: Path, schematic_path: str, output: str, source: str
) -> dict[str, object]:
    """Insert a ``.tf`` directive."""

    return _edit_directive(
        workspace_root, schematic_path, f".tf {output} {source}", comment_other_analyses=True
    )


def prepare_four(
    *, workspace_root: Path, schematic_path: str, frequency: str, traces: str
) -> dict[str, object]:
    """Insert a ``.four`` directive."""

    return _edit_directive(workspace_root, schematic_path, f".four {frequency} {traces}")


def prepare_meas(*, workspace_root: Path, schematic_path: str, statement: str) -> dict[str, object]:
    """Insert a ``.meas`` directive. Do not replace the other measurements."""

    body = statement.strip()
    if not body.lower().startswith(".meas"):
        body = f".meas {body}"
    path, schematic, previous = _schematic(workspace_root, schematic_path)
    result = upsert_directive(
        schematic, body, replace_command=f"meas-unique-{len(schematic.texts())}"
    )
    result.update(_store(path, schematic, previous))
    return result


def prepare_save(*, workspace_root: Path, schematic_path: str, traces: str) -> dict[str, object]:
    """Insert a ``.save`` directive."""

    return _edit_directive(workspace_root, schematic_path, f".save {traces}")


def prepare_options(
    *, workspace_root: Path, schematic_path: str, options: str
) -> dict[str, object]:
    """Insert a ``.options`` directive."""

    return _edit_directive(workspace_root, schematic_path, f".options {options}")


def prepare_temperature_sweep(
    *,
    workspace_root: Path,
    schematic_path: str,
    start: str,
    stop: str,
    step: str,
) -> dict[str, object]:
    """Insert a ``.step temp`` directive."""

    return _edit_directive(workspace_root, schematic_path, f".step temp {start} {stop} {step}")


def prepare_net(
    *,
    workspace_root: Path,
    schematic_path: str,
    output: str,
    source: str,
    rin: str = "",
    rout: str = "",
) -> dict[str, object]:
    """Insert a ``.net`` network-parameter directive."""

    extra = ""
    if rin:
        extra += f" Rin={rin}"
    if rout:
        extra += f" Rout={rout}"
    return _edit_directive(workspace_root, schematic_path, f".net {output} {source}{extra}")


def prepare_step(*, workspace_root: Path, schematic_path: str, statement: str) -> dict[str, object]:
    """Insert a ``.step`` directive."""

    body = statement if statement.strip().lower().startswith(".step") else f".step {statement}"
    return _edit_directive(workspace_root, schematic_path, body)


def prepare_param(
    *, workspace_root: Path, schematic_path: str, name: str, value: str
) -> dict[str, object]:
    """Insert a ``.param`` directive."""

    return _edit_directive(workspace_root, schematic_path, f".param {name}={value}")


def prepare_func(
    *, workspace_root: Path, schematic_path: str, definition: str
) -> dict[str, object]:
    """Insert a ``.func`` directive."""

    body = definition if definition.strip().lower().startswith(".func") else f".func {definition}"
    return _edit_directive(workspace_root, schematic_path, body)


def prepare_ic(*, workspace_root: Path, schematic_path: str, assignments: str) -> dict[str, object]:
    """Insert a ``.ic`` directive."""

    return _edit_directive(workspace_root, schematic_path, f".ic {assignments}")


def prepare_nodeset(
    *, workspace_root: Path, schematic_path: str, assignments: str
) -> dict[str, object]:
    """Insert a ``.nodeset`` directive."""

    return _edit_directive(workspace_root, schematic_path, f".nodeset {assignments}")


def list_plot_suggestions(*, workspace_root: Path, schematic_path: str) -> dict[str, object]:
    """Suggest voltages and currents an agent can plot."""

    _path, schematic, _previous = _schematic(workspace_root, schematic_path)
    flags = [f"V({flag.name})" for flag in schematic.flags() if flag.name != "0"]
    currents = [f"I({symbol.reference()})" for symbol in schematic.symbols() if symbol.reference()]
    return {"voltages": flags, "currents": currents}


def run_simulation_service(
    *,
    workspace_root: Path,
    source_path: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
    ascii_raw: bool = True,
    timeout_s: float | None = None,
    extra_switches: tuple[str, ...] | None = None,
) -> dict[str, object]:
    """Run one batch simulation."""

    source = _source(workspace_root, source_path)
    effective = settings or LTspiceSettings(workspace_root=workspace_root)
    result = run_simulation(
        source,
        settings=effective,
        executable=ltspice_executable,
        ascii_raw=ascii_raw,
        timeout_s=timeout_s,
        extra_switches=tuple(extra_switches or ()),
    )
    result["source_path"] = str(source)
    return result


def cancel_run(*, workspace_root: Path, source_path: str) -> dict[str, object]:
    """Stop a simulation started for this source path."""

    source = resolve_workspace_path(source_path, workspace_root=workspace_root)
    process = lookup_run(str(source.resolve()))
    if process is None:
        return {"cancelled": False, "reason": "No simulation is running for that path."}
    _kill_process_tree(process)
    pop_run(str(source.resolve()))
    return {"cancelled": True, "pid": process.pid}


def _run_many(
    workspace_root: Path,
    schematic_path: str,
    settings: LTspiceSettings | None,
    ltspice_executable: Path | None,
    cases: list[tuple[str, str]],
) -> dict[str, object]:
    results: list[dict[str, object]] = []
    for reference, value in cases:
        path, schematic, previous = _schematic(workspace_root, schematic_path)
        set_component_value(schematic, reference, value)
        _store(path, schematic, previous)
        results.append(
            {
                "value": value,
                "run": run_simulation_service(
                    workspace_root=workspace_root,
                    source_path=schematic_path,
                    settings=settings,
                    ltspice_executable=ltspice_executable,
                ),
            }
        )
    return {"runs": results}


def run_value_sweep(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    values: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Run the schematic once per component value."""

    cases = [(reference, item.strip()) for item in values.split(",") if item.strip()]
    if not cases:
        raise ValidationError("values must be a comma-separated list.")
    return _run_many(workspace_root, schematic_path, settings, ltspice_executable, cases)


def run_param_sweep(
    *,
    workspace_root: Path,
    schematic_path: str,
    statement: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Add a ``.step`` and run once. LTspice expands the steps."""

    prepare_step(workspace_root=workspace_root, schematic_path=schematic_path, statement=statement)
    return run_simulation_service(
        workspace_root=workspace_root,
        source_path=schematic_path,
        settings=settings,
        ltspice_executable=ltspice_executable,
    )


def run_model_sweep(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    models: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Run once per model name."""

    results: list[dict[str, object]] = []
    for model in [item.strip() for item in models.split(",") if item.strip()]:
        path, schematic, previous = _schematic(workspace_root, schematic_path)
        set_element_model(schematic, reference, model)
        _store(path, schematic, previous)
        results.append(
            {
                "model": model,
                "run": run_simulation_service(
                    workspace_root=workspace_root,
                    source_path=schematic_path,
                    settings=settings,
                    ltspice_executable=ltspice_executable,
                ),
            }
        )
    return {"runs": results}


def prepare_monte_carlo(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    nominal: str,
    tolerance: str,
    runs: int = 20,
) -> dict[str, object]:
    """Point a component at ``mc()`` and step the run index."""

    path, schematic, previous = _schematic(workspace_root, schematic_path)
    set_component_value(schematic, reference, "{mcval}")
    _store(path, schematic, previous)
    upsert = prepare_param(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        name="mcval",
        value=f"{{mc({nominal},{tolerance})}}",
    )
    stepped = prepare_step(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        statement=f"param run 1 {runs} 1",
    )
    return {"reference": reference, "param": upsert, "step": stepped, "runs": runs}


def run_monte_carlo(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    nominal: str,
    tolerance: str,
    runs: int = 20,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Prepare a Monte Carlo ``.step`` and run it."""

    prepared = prepare_monte_carlo(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        reference=reference,
        nominal=nominal,
        tolerance=tolerance,
        runs=runs,
    )
    simulated = run_simulation_service(
        workspace_root=workspace_root,
        source_path=schematic_path,
        settings=settings,
        ltspice_executable=ltspice_executable,
    )
    return {"prepared": prepared, "run": simulated}


def summarize_tolerance_analysis(
    *, workspace_root: Path, raw_path: str, signal: str
) -> dict[str, object]:
    """Summarize min, max, and mean of a stepped trace."""

    path = validate_existing_file(raw_path, workspace_root=workspace_root, suffixes=(".raw",))
    plot = load_primary(path)
    column = find_signal(plot, signal)
    spans = split_steps(plot)
    means = [float(plot.real[start:stop, column].mean()) for start, stop in spans if stop > start]
    if not means:
        raise ArtifactMissingError("No samples were available to summarize.")
    return {
        "signal": signal,
        "steps": len(means),
        "min": min(means),
        "max": max(means),
        "mean": sum(means) / len(means),
    }


def prepare_loop_gain_analysis(
    *,
    workspace_root: Path,
    schematic_path: str,
    injection_source: str = "",
    f_start: str = "10",
    f_end: str = "1Meg",
) -> dict[str, object]:
    """Stage an AC loop-gain run. Use the extra-source method.

    The injection source, when named, receives ``AC 1``. Place that source in the
    feedback loop. Gain is ``V(out)/V(err)`` once those nets exist.
    """

    ac = prepare_ac(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        f_start=f_start,
        f_end=f_end,
    )
    note = "Place a voltage source in the feedback path and give it an AC 1 stimulus."
    if injection_source:
        path, schematic, previous = _schematic(workspace_root, schematic_path)
        symbol = schematic.find_symbol(injection_source)
        value = symbol.attr("Value") or "0"
        if "ac" not in value.lower():
            symbol.set_attr("Value", f"{value} AC 1")
            _store(path, schematic, previous)
        note = f"{injection_source} now includes AC 1."
    return {"ac": ac, "method": "middlebrook-tian-extra-source", "note": note}


def prepare_worst_case(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    low: str,
    high: str,
) -> dict[str, object]:
    """Step a component between two corner values with ``table()``."""

    path, schematic, previous = _schematic(workspace_root, schematic_path)
    set_component_value(schematic, reference, "{corner_value}")
    _store(path, schematic, previous)
    prepare_param(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        name="corner_value",
        value=f"{{table(corner,1,{low},2,{high})}}",
    )
    return prepare_step(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        statement="param corner 1 2 1",
    )


def run_worst_case(
    *,
    workspace_root: Path,
    schematic_path: str,
    reference: str,
    low: str,
    high: str,
    settings: LTspiceSettings | None = None,
    ltspice_executable: Path | None = None,
) -> dict[str, object]:
    """Prepare two corners and run them."""

    prepared = prepare_worst_case(
        workspace_root=workspace_root,
        schematic_path=schematic_path,
        reference=reference,
        low=low,
        high=high,
    )
    simulated = run_simulation_service(
        workspace_root=workspace_root,
        source_path=schematic_path,
        settings=settings,
        ltspice_executable=ltspice_executable,
    )
    return {"prepared": prepared, "run": simulated}
