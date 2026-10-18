# In the name of God, the Most Gracious, the Most Merciful
"""Artifact export use cases. Exports are pure Python; LTspice has no QUX helper."""

from __future__ import annotations

import csv
from typing import TYPE_CHECKING

import numpy as np

from ltspice_mcp.services._backends.log_parse import parse_measures, read_log_text
from ltspice_mcp.services._backends.waveform_math import (
    column_complex,
    find_signal,
    load_primary,
    trace_payload,
)
from ltspice_mcp.services._shared.paths import (
    resolve_output_path,
    resolve_workspace_path,
    validate_existing_file,
)

if TYPE_CHECKING:
    from pathlib import Path


def _raw(workspace_root: Path, raw_path: str) -> Path:
    return validate_existing_file(raw_path, workspace_root=workspace_root, suffixes=(".raw",))


def export_waveform_csv(
    *,
    workspace_root: Path,
    raw_path: str,
    signals: str,
    output_path: str = "",
) -> dict[str, object]:
    """Write selected signals to CSV."""

    source = _raw(workspace_root, raw_path)
    plot = load_primary(source)
    names = [item.strip() for item in signals.split(",") if item.strip()]
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_suffix(".csv"),
        suffixes=(".csv",),
    )
    columns = [plot.real[:, 0]]
    header = [plot.variables[0].name]
    for name in names:
        columns.append(np.real(column_complex(plot, find_signal(plot, name))))
        header.append(name)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for row in zip(*columns, strict=True):
            writer.writerow([f"{float(value):.9g}" for value in row])
    return {"path": str(destination), "rows": int(plot.real.shape[0]), "signals": names}


def export_waveform_ascii(
    *, workspace_root: Path, raw_path: str, signal: str, output_path: str = ""
) -> dict[str, object]:
    """Write one signal as whitespace-separated text."""

    source = _raw(workspace_root, raw_path)
    payload = trace_payload(load_primary(source), signal, max_points=2000)
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_name(source.stem + ".txt"),
        suffixes=(".txt",),
    )
    real = payload["real"]
    x_values = payload["x"]
    if not isinstance(real, list) or not isinstance(x_values, list):
        raise TypeError("Trace payload was not a list.")
    lines = [f"{x} {y}" for x, y in zip(x_values, real, strict=True)]
    destination.write_text("\n".join(str(line) for line in lines) + "\n", encoding="utf-8")
    return {"path": str(destination), "points": len(lines)}


def export_waveform_spice(
    *, workspace_root: Path, raw_path: str, signal: str, output_path: str = ""
) -> dict[str, object]:
    """Write a PWL statement for one real trace."""

    source = _raw(workspace_root, raw_path)
    payload = trace_payload(load_primary(source), signal, max_points=500)
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_name(source.stem + ".pwl"),
        suffixes=(".pwl", ".cir"),
    )
    real = payload["real"]
    x_values = payload["x"]
    if not isinstance(real, list) or not isinstance(x_values, list):
        raise TypeError("Trace payload was not a list.")
    pairs = " ".join(f"{x},{y}" for x, y in zip(x_values, real, strict=True))
    destination.write_text(f"PWL({pairs})\n", encoding="utf-8")
    return {"path": str(destination)}


def export_touchstone_s2p(
    *,
    workspace_root: Path,
    raw_path: str,
    output_signal: str,
    reference_signal: str,
    output_path: str = "",
    z0: float = 50.0,
) -> dict[str, object]:
    """Write a one-port-style S2P using S21 = output/reference and the other terms at 0.

    This is a derived export for AC data, not a substitute for a ``.net`` two-port run.
    """

    source = _raw(workspace_root, raw_path)
    plot = load_primary(source)
    ratio = column_complex(plot, find_signal(plot, output_signal)) / column_complex(
        plot, find_signal(plot, reference_signal)
    )
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_suffix(".s2p"),
        suffixes=(".s2p",),
    )
    lines = [
        "! ltspice-mcp derived Touchstone. S21 is output/reference; S11=S22=S12=0.",
        f"# HZ S RI R {z0}",
    ]
    for frequency, value in zip(plot.real[:, 0], ratio, strict=True):
        lines.append(f"{frequency:.9g} 0 0 {value.real:.9g} {value.imag:.9g} 0 0 0 0")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": str(destination), "rows": int(plot.real.shape[0])}


def export_derived_raw(
    *, workspace_root: Path, raw_path: str, signal: str, output_path: str = ""
) -> dict[str, object]:
    """Write a small ASCII raw file containing one trace."""

    source = _raw(workspace_root, raw_path)
    payload = trace_payload(load_primary(source), signal, max_points=2000)
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_name(source.stem + "-derived.raw"),
        suffixes=(".raw",),
    )
    real = payload["real"]
    x_values = payload["x"]
    if not isinstance(real, list) or not isinstance(x_values, list):
        raise TypeError("Trace payload was not a list.")
    lines = [
        "Title: ltspice-mcp derived",
        "Plotname: Derived",
        "Flags: real",
        "No. Variables: 2",
        f"No. Points: {len(x_values)}",
        "Variables:",
        f"\t0\t{payload['x_name']}\ttime",
        f"\t1\t{signal}\tvoltage",
        "Values:",
    ]
    for index, (x_value, y_value) in enumerate(zip(x_values, real, strict=True)):
        lines.append(f"{index}\t{x_value}")
        lines.append(f"\t{y_value}")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": str(destination), "points": len(x_values)}


def merge_waveforms(
    *, workspace_root: Path, left_path: str, right_path: str, signal: str
) -> dict[str, object]:
    """Return two traces side by side without writing a combined raw file."""

    left = trace_payload(load_primary(_raw(workspace_root, left_path)), signal, max_points=500)
    right = trace_payload(load_primary(_raw(workspace_root, right_path)), signal, max_points=500)
    return {"signal": signal, "left": left, "right": right}


def compare_waveforms(
    *, workspace_root: Path, left_path: str, right_path: str, signal: str
) -> dict[str, object]:
    """Compare the means of one signal in two raw files."""

    left = load_primary(_raw(workspace_root, left_path))
    right = load_primary(_raw(workspace_root, right_path))
    left_values = np.real(column_complex(left, find_signal(left, signal)))
    right_values = np.real(column_complex(right, find_signal(right, signal)))
    count = min(len(left_values), len(right_values))
    if count == 0:
        return {"signal": signal, "rmse": None, "points": 0}
    delta = left_values[:count] - right_values[:count]
    rmse = float(np.sqrt(np.mean(delta**2)))
    return {"signal": signal, "rmse": rmse, "points": count}


def export_measures_csv(
    *, workspace_root: Path, log_path: str, output_path: str = ""
) -> dict[str, object]:
    """Write ``.meas`` rows to CSV."""

    source = validate_existing_file(log_path, workspace_root=workspace_root, suffixes=(".log",))
    measures = parse_measures(read_log_text(source))
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_suffix(".csv"),
        suffixes=(".csv",),
    )
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["name", "detail"])
        for item in measures:
            writer.writerow([item.get("name", ""), str(item)])
    return {"path": str(destination), "rows": len(measures)}


def summarize_batch(*, workspace_root: Path, batch_dir: str) -> dict[str, object]:
    """Summarize raw files sitting in a batch directory."""

    resolved = resolve_workspace_path(batch_dir, workspace_root=workspace_root)
    if not resolved.is_dir():
        return {"path": str(resolved), "raw_files": [], "note": "Batch directory does not exist."}
    raws = sorted(str(path) for path in resolved.glob("*.raw"))
    return {"path": str(resolved), "raw_files": raws, "count": len(raws)}
