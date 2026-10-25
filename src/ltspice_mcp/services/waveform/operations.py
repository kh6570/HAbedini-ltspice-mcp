# In the name of God, the Most Gracious, the Most Merciful
"""Waveform use cases."""

from __future__ import annotations

from io import BytesIO

import matplotlib

matplotlib.use("Agg", force=True)
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from mcp_app_core.images import ImageResult

from ltspice_mcp.core.exceptions import ValidationError
from ltspice_mcp.services._backends.log_parse import (
    log_summary,
    operating_point_report,
    parse_fourier,
    parse_measures,
    parse_noise,
    parse_steps,
    read_log_text,
)
from ltspice_mcp.services._backends.waveform_math import (
    bode,
    column_complex,
    evaluate_expression,
    fft_spectrum,
    find_signal,
    load_primary,
    scalar_measure,
    split_steps,
    stability_margins,
    step_response,
    thd,
    trace_payload,
)
from ltspice_mcp.services._shared.paths import resolve_output_path, validate_existing_file

if TYPE_CHECKING:
    from pathlib import Path


def _raw(workspace_root: Path, raw_path: str) -> Path:
    return validate_existing_file(raw_path, workspace_root=workspace_root, suffixes=(".raw",))


def _log(workspace_root: Path, log_path: str) -> Path:
    return validate_existing_file(log_path, workspace_root=workspace_root, suffixes=(".log",))


def list_signals(*, workspace_root: Path, raw_path: str) -> dict[str, object]:
    """List signals in a raw file."""

    plot = load_primary(_raw(workspace_root, raw_path))
    return {
        "plotname": plot.plotname,
        "flags": sorted(plot.flags),
        "points": int(plot.real.shape[0]),
        "signals": [{"name": variable.name, "type": variable.kind} for variable in plot.variables],
    }


def list_steps(*, workspace_root: Path, raw_path: str, log_path: str = "") -> dict[str, object]:
    """List stepped runs from a raw file and, when given, the log."""

    plot = load_primary(_raw(workspace_root, raw_path))
    spans = split_steps(plot)
    steps = [
        {"index": index, "start": start, "stop": stop} for index, (start, stop) in enumerate(spans)
    ]
    logged: list[str] = []
    if log_path:
        logged = parse_steps(read_log_text(_log(workspace_root, log_path)))
    return {"raw_steps": steps, "log_steps": logged}


def read_waveform(
    *,
    workspace_root: Path,
    raw_path: str,
    signal: str,
    t_start: float | None = None,
    t_end: float | None = None,
    max_points: int = 2000,
) -> dict[str, object]:
    """Read one budgeted waveform."""

    plot = load_primary(_raw(workspace_root, raw_path))
    return trace_payload(plot, signal, max_points=max_points, t_start=t_start, t_end=t_end)


def evaluate_waveform_expression(
    *, workspace_root: Path, raw_path: str, expression: str, max_points: int = 2000
) -> dict[str, object]:
    """Evaluate an expression built from raw signal names."""

    plot = load_primary(_raw(workspace_root, raw_path))
    values = evaluate_expression(plot, expression)
    payload = trace_payload(plot, plot.variables[0].name, max_points=max_points)
    point_count = payload["points"]
    if not isinstance(point_count, int):
        raise ValidationError("Waveform point count was not an integer.")
    limited = values[:point_count]
    return {
        "expression": expression,
        "x": payload["x"],
        "real": [float(np.real(value)) for value in limited],
        "imag": [float(np.imag(value)) for value in limited],
    }


def measure_waveform(
    *, workspace_root: Path, raw_path: str, signal: str, method: str
) -> dict[str, object]:
    """Measure avg, rms, max, min, pp, or peak."""

    return scalar_measure(load_primary(_raw(workspace_root, raw_path)), signal, method)


def measure_bode_response(
    *, workspace_root: Path, raw_path: str, output: str, reference: str
) -> dict[str, object]:
    """Bode magnitude and phase of output/reference."""

    return bode(load_primary(_raw(workspace_root, raw_path)), output, reference)


def measure_stability_margins(
    *, workspace_root: Path, raw_path: str, output: str, reference: str
) -> dict[str, object]:
    """Gain and phase margins."""

    return stability_margins(load_primary(_raw(workspace_root, raw_path)), output, reference)


def measure_step_response(*, workspace_root: Path, raw_path: str, signal: str) -> dict[str, object]:
    """Step-response scalars."""

    return step_response(load_primary(_raw(workspace_root, raw_path)), signal)


def measure_efficiency(
    *,
    workspace_root: Path,
    raw_path: str,
    v_in: str,
    i_in: str,
    v_out: str,
    i_out: str,
) -> dict[str, object]:
    """Average output power over average input power."""

    plot = load_primary(_raw(workspace_root, raw_path))
    vin = np.real(column_complex(plot, find_signal(plot, v_in)))
    iin = np.real(column_complex(plot, find_signal(plot, i_in)))
    vout = np.real(column_complex(plot, find_signal(plot, v_out)))
    iout = np.real(column_complex(plot, find_signal(plot, i_out)))
    pin = float(np.mean(vin * iin))
    pout = float(np.mean(vout * iout))
    efficiency = None if abs(pin) < 1e-18 else pout / pin
    return {"input_power": pin, "output_power": pout, "efficiency": efficiency}


def compute_thd(
    *, workspace_root: Path, raw_path: str, signal: str, fundamental_hz: float
) -> dict[str, object]:
    """Total harmonic distortion."""

    return thd(load_primary(_raw(workspace_root, raw_path)), signal, fundamental_hz)


def export_fft_spectrum(
    *,
    workspace_root: Path,
    raw_path: str,
    signal: str,
    output_path: str = "",
) -> dict[str, object]:
    """Write an FFT magnitude CSV."""

    source = _raw(workspace_root, raw_path)
    freqs, mags = fft_spectrum(load_primary(source), signal)
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_name(source.stem + "-fft.csv"),
        suffixes=(".csv",),
    )
    lines = ["frequency_hz,magnitude"]
    lines.extend(f"{freq},{mag}" for freq, mag in zip(freqs, mags, strict=True))
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": str(destination), "bins": len(freqs)}


def plot_waveforms(
    *,
    workspace_root: Path,
    raw_path: str,
    signals: str,
    output_path: str = "",
) -> dict[str, object]:
    """Plot one or more comma-separated signals to a PNG."""

    source = _raw(workspace_root, raw_path)
    plot = load_primary(source)
    names = [item.strip() for item in signals.split(",") if item.strip()]
    figure, axis = plt.subplots(figsize=(8, 4))
    for name in names:
        payload = trace_payload(plot, name, max_points=2000)
        x_values = payload["x"]
        y_values = payload["real"]
        if not isinstance(x_values, list) or not isinstance(y_values, list):
            raise ValidationError("Waveform payload was not a list.")
        axis.plot(x_values, y_values, label=name)
    axis.legend()
    axis.set_xlabel(str(plot.variables[0].name))
    axis.grid(True)
    destination = resolve_output_path(
        output_path or None,
        workspace_root=workspace_root,
        default=source.with_suffix(".png"),
        suffixes=(".png",),
    )
    figure.tight_layout()
    buffer = BytesIO()
    figure.savefig(buffer, format="png", dpi=100)
    plt.close(figure)
    png = buffer.getvalue()
    destination.write_bytes(png)
    summary = f"Plotted {', '.join(names)} from {source.name}."
    if len(summary) > 280:
        summary = f"Plotted {len(names)} signals from {source.name}."
    image = ImageResult(png=png, summary=summary)
    return {"path": str(destination), "signals": names, **image.as_dict()}


def read_log(*, workspace_root: Path, log_path: str) -> dict[str, object]:
    """Summarize a simulation log."""

    return log_summary(_log(workspace_root, log_path))


def read_fourier(*, workspace_root: Path, log_path: str) -> dict[str, object]:
    """Read the Fourier section of a log."""

    return parse_fourier(read_log_text(_log(workspace_root, log_path)))


def read_noise(*, workspace_root: Path, log_path: str) -> dict[str, object]:
    """Read noise lines from a log."""

    return parse_noise(read_log_text(_log(workspace_root, log_path)))


def list_measures(*, workspace_root: Path, log_path: str) -> dict[str, object]:
    """List ``.meas`` names."""

    measures = parse_measures(read_log_text(_log(workspace_root, log_path)))
    return {"measures": [item.get("name") for item in measures]}


def read_measures(*, workspace_root: Path, log_path: str) -> dict[str, object]:
    """Read ``.meas`` results."""

    return {"measures": parse_measures(read_log_text(_log(workspace_root, log_path)))}


def _point_rows(report: dict[str, object]) -> list[dict[str, object]]:
    rows = report.get("points")
    if not isinstance(rows, list):
        raise ValidationError("Operating-point rows were not a list.")
    typed: list[dict[str, object]] = []
    for row in rows:
        if isinstance(row, dict):
            typed.append({str(key): value for key, value in row.items()})
    return typed


def read_device_operating_points(*, workspace_root: Path, log_path: str) -> dict[str, object]:
    """Read operating-point rows from a log and a sibling ``.op.raw`` when present."""

    return operating_point_report(_log(workspace_root, log_path))


def filter_device_operating_points(
    *, workspace_root: Path, log_path: str, device: str
) -> dict[str, object]:
    """Keep operating-point rows whose name contains ``device``."""

    rows = _point_rows(operating_point_report(_log(workspace_root, log_path)))
    needle = device.lower()
    return {"points": [row for row in rows if needle in str(row["name"]).lower()]}


def summarize_device_operating_points(*, workspace_root: Path, log_path: str) -> dict[str, object]:
    """Count operating-point rows by unit."""

    rows = _point_rows(operating_point_report(_log(workspace_root, log_path)))
    units: dict[str, int] = {}
    for row in rows:
        unit = str(row["unit"])
        units[unit] = units.get(unit, 0) + 1
    return {"count": len(rows), "units": units}
