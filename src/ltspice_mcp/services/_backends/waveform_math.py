# In the name of God, the Most Gracious, the Most Merciful
"""Waveform math that does not depend on the LTspice executable."""

from __future__ import annotations

import ast
import math
from typing import TYPE_CHECKING

import numpy as np

from ltspice_mcp.core.budgets import DEFAULT_BUDGET, DataBudget, downsample_indices
from ltspice_mcp.core.exceptions import ParseError, ValidationError
from ltspice_mcp.services._backends.raw_file import RawPlot, load_raw

if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray

_FUNCS = {
    "abs": np.abs,
    "mag": np.abs,
    "db": lambda value: 20.0 * np.log10(np.maximum(np.abs(value), 1e-30)),
    "ph": lambda value: np.degrees(np.angle(value)),
    "re": np.real,
    "im": np.imag,
    "sqrt": np.sqrt,
    "log": np.log,
    "log10": np.log10,
    "exp": np.exp,
}


def load_primary(path: Path) -> RawPlot:
    """Load the first plot in a raw file."""

    return load_raw(path).primary


def find_signal(plot: RawPlot, name: str) -> int:
    """Return the column index for a signal name."""

    wanted = name.strip()
    for variable in plot.variables:
        if variable.name.lower() == wanted.lower():
            return variable.index
    raise ValidationError(f"Signal {name!r} was not found. Available: {', '.join(plot.names())}")


def column_complex(plot: RawPlot, index: int) -> NDArray[np.complex128]:
    """Return one column as complex samples."""

    real = plot.real[:, index]
    if plot.imag is None:
        return real.astype(np.complex128)
    return real + 1j * plot.imag[:, index]


def apply_budget(
    x_values: NDArray[np.float64],
    y_values: NDArray[np.complex128],
    *,
    budget: DataBudget | None = None,
    max_points: int | None = None,
) -> tuple[list[float], list[float], list[float] | None, bool]:
    """Downsample a trace to the data budget."""

    active = budget or DEFAULT_BUDGET
    if max_points is not None:
        active = DataBudget(
            max_points=max_points, max_bytes=active.max_bytes, strategy=active.strategy
        )
    target = active.target_points(len(x_values))
    indices = downsample_indices(
        len(x_values), max(target, 2) if len(x_values) >= 2 else len(x_values)
    )
    if len(x_values) >= 2 and len(indices) < 2:
        raise ParseError("Waveform budget left fewer than two points.")
    xs = [float(x_values[index]) for index in indices]
    real = [float(np.real(y_values[index])) for index in indices]
    imag = None
    if np.any(np.imag(y_values)):
        imag = [float(np.imag(y_values[index])) for index in indices]
    return xs, real, imag, len(indices) != len(x_values)


def trace_payload(
    plot: RawPlot,
    name: str,
    *,
    max_points: int | None = None,
    t_start: float | None = None,
    t_end: float | None = None,
) -> dict[str, object]:
    """Return one budgeted trace."""

    if t_start is not None and t_end is not None and t_end < t_start:
        raise ValidationError("t_end must be greater than or equal to t_start")
    index = find_signal(plot, name)
    x_name = plot.variables[0].name
    x_values = plot.real[:, 0]
    y_values = column_complex(plot, index)
    if t_start is not None or t_end is not None:
        mask = np.ones(len(x_values), dtype=bool)
        if t_start is not None:
            mask &= x_values >= t_start
        if t_end is not None:
            mask &= x_values <= t_end
        x_values = x_values[mask]
        y_values = y_values[mask]
    if len(x_values) == 0:
        raise ValidationError("The requested window contains no samples.")
    xs, real, imag, downsampled = apply_budget(x_values, y_values, max_points=max_points)
    return {
        "signal": plot.variables[index].name,
        "x_name": x_name,
        "x": xs,
        "real": real,
        "imag": imag,
        "points": len(xs),
        "source_points": int(plot.real.shape[0]),
        "downsampled": downsampled,
        "complex": imag is not None,
        "plotname": plot.plotname,
    }


def scalar_measure(plot: RawPlot, name: str, method: str) -> dict[str, object]:
    """Compute a scalar measurement on one real trace."""

    index = find_signal(plot, name)
    values = np.real(column_complex(plot, index))
    x_values = plot.real[:, 0]
    key = method.strip().lower()
    if key in {"avg", "average", "mean"}:
        result = float(np.mean(values))
    elif key == "rms":
        result = float(np.sqrt(np.mean(values**2)))
    elif key == "max":
        result = float(np.max(values))
    elif key == "min":
        result = float(np.min(values))
    elif key in {"pp", "peak_to_peak"}:
        result = float(np.max(values) - np.min(values))
    elif key == "peak":
        result = float(np.max(np.abs(values)))
    else:
        raise ValidationError("method must be avg, rms, max, min, pp, or peak.")
    return {
        "signal": plot.variables[index].name,
        "method": key,
        "value": result,
        "x_start": float(x_values[0]),
        "x_end": float(x_values[-1]),
    }


def _eval_node(node: ast.AST, env: dict[str, NDArray[np.complex128]]) -> NDArray[np.complex128]:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return np.full(next(iter(env.values())).shape, float(node.value), dtype=np.complex128)
    if isinstance(node, ast.Name):
        key = node.id.lower()
        if key not in env:
            raise ValidationError(f"Unknown name {node.id!r} in waveform expression.")
        return env[key]
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, env)
        if isinstance(node.op, ast.USub):
            return np.asarray(-operand, dtype=np.complex128)
        if isinstance(node.op, ast.UAdd):
            return np.asarray(+operand, dtype=np.complex128)
        raise ValidationError("Unsupported unary operator.")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, env)
        right = _eval_node(node.right, env)
        if isinstance(node.op, ast.Add):
            return np.asarray(left + right, dtype=np.complex128)
        if isinstance(node.op, ast.Sub):
            return np.asarray(left - right, dtype=np.complex128)
        if isinstance(node.op, ast.Mult):
            return np.asarray(left * right, dtype=np.complex128)
        if isinstance(node.op, ast.Div):
            return np.asarray(left / right, dtype=np.complex128)
        if isinstance(node.op, ast.Pow):
            return np.asarray(left**right, dtype=np.complex128)
        raise ValidationError("Unsupported binary operator.")
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        func_name = node.func.id.lower()
        if func_name not in _FUNCS or len(node.args) != 1:
            raise ValidationError(f"Unsupported function in expression: {ast.unparse(node)}")
        raw_func = _FUNCS[func_name]
        return np.asarray(raw_func(_eval_node(node.args[0], env)), dtype=np.complex128)  # type: ignore[operator]
    raise ValidationError(f"Unsupported expression syntax: {ast.unparse(node)}")


def evaluate_expression(plot: RawPlot, expression: str) -> NDArray[np.complex128]:
    """Evaluate a small arithmetic expression over raw columns.

    Names are signal names with parentheses removed, so ``V(out)`` is ``Vout``
    is not required: the call syntax ``V(out)`` is rewritten to a lookup of the
    raw column ``V(out)``.
    """

    rewritten = expression.strip()
    env: dict[str, NDArray[np.complex128]] = {}
    for variable in plot.variables:
        token = f"s{variable.index}"
        env[token] = column_complex(plot, variable.index)
        rewritten = rewritten.replace(variable.name, token)
    try:
        tree = ast.parse(rewritten, mode="eval")
    except SyntaxError as exc:
        raise ValidationError(f"Could not parse expression: {exc.msg}") from exc
    return _eval_node(tree, env)


def bode(plot: RawPlot, output: str, reference: str) -> dict[str, object]:
    """Magnitude in dB and phase in degrees of output/reference."""

    ratio = column_complex(plot, find_signal(plot, output)) / column_complex(
        plot, find_signal(plot, reference)
    )
    frequency = plot.real[:, 0]
    magnitude = 20.0 * np.log10(np.maximum(np.abs(ratio), 1e-30))
    phase = np.degrees(np.angle(ratio))
    return {
        "frequency": [float(value) for value in frequency],
        "magnitude_db": [float(value) for value in magnitude],
        "phase_deg": [float(value) for value in phase],
    }


def _crossing(
    x_values: NDArray[np.float64], y_values: NDArray[np.float64], level: float
) -> float | None:
    for index in range(len(y_values) - 1):
        left, right = float(y_values[index]), float(y_values[index + 1])
        if (left - level) == 0:
            return float(x_values[index])
        if (left - level) * (right - level) < 0:
            span = right - left
            if span == 0:
                continue
            fraction = (level - left) / span
            return float(x_values[index] + fraction * (x_values[index + 1] - x_values[index]))
    return None


def stability_margins(plot: RawPlot, output: str, reference: str) -> dict[str, object]:
    """Gain and phase margins from a loop-gain AC trace."""

    response = bode(plot, output, reference)
    frequency = np.asarray(response["frequency"], dtype=np.float64)
    magnitude = np.asarray(response["magnitude_db"], dtype=np.float64)
    phase = np.asarray(response["phase_deg"], dtype=np.float64)
    gain_crossover = _crossing(frequency, magnitude, 0.0)
    phase_crossover = _crossing(frequency, phase, -180.0)
    phase_margin = None
    gain_margin = None
    if gain_crossover is not None:
        phase_margin = float(np.interp(gain_crossover, frequency, phase) + 180.0)
    if phase_crossover is not None:
        gain_margin = float(-np.interp(phase_crossover, frequency, magnitude))
    return {
        "gain_crossover_hz": gain_crossover,
        "phase_crossover_hz": phase_crossover,
        "phase_margin_deg": phase_margin,
        "gain_margin_db": gain_margin,
    }


def step_response(plot: RawPlot, name: str) -> dict[str, object]:
    """Rise time, overshoot, and 2 percent settling time of a real step."""

    index = find_signal(plot, name)
    time = plot.real[:, 0]
    values = np.real(column_complex(plot, index))
    start = float(values[0])
    final = float(np.mean(values[int(len(values) * 0.8) :]))
    delta = final - start
    if abs(delta) < 1e-15:
        raise ValidationError("The trace does not move enough to measure a step.")
    normalized = (values - start) / delta
    ten = _crossing(time, normalized, 0.1)
    ninety = _crossing(time, normalized, 0.9)
    rise = None if ten is None or ninety is None else ninety - ten
    peak = float(np.max(normalized))
    overshoot = max(0.0, peak - 1.0) * 100.0
    settled = None
    band = 0.02
    for index_sample in range(len(normalized) - 1, -1, -1):
        if abs(float(normalized[index_sample]) - 1.0) > band:
            if index_sample + 1 < len(time):
                settled = float(time[index_sample + 1])
            break
    return {
        "signal": plot.variables[index].name,
        "rise_time_s": rise,
        "overshoot_percent": overshoot,
        "settling_time_s": settled,
        "initial": start,
        "final": final,
    }


def thd(plot: RawPlot, name: str, fundamental_hz: float) -> dict[str, object]:
    """Total harmonic distortion from a real transient trace."""

    if fundamental_hz <= 0:
        raise ValidationError("fundamental_hz must be positive.")
    index = find_signal(plot, name)
    time = plot.real[:, 0]
    values = np.real(column_complex(plot, index))
    if len(values) < 8:
        raise ValidationError("Need at least 8 samples to compute THD.")
    centered = values - np.mean(values)
    spectrum = np.fft.rfft(centered)
    freqs = np.fft.rfftfreq(len(centered), d=float(np.mean(np.diff(time))))
    magnitudes = np.abs(spectrum)
    fundamental_bin = int(np.argmin(np.abs(freqs - fundamental_hz)))
    fundamental = float(magnitudes[fundamental_bin])
    if fundamental == 0:
        raise ValidationError("The fundamental bin is empty.")
    harmonic_power = 0.0
    for harmonic in range(2, 11):
        target = fundamental_hz * harmonic
        if target > float(freqs[-1]):
            break
        bucket = int(np.argmin(np.abs(freqs - target)))
        harmonic_power += float(magnitudes[bucket] ** 2)
    ratio = math.sqrt(harmonic_power) / fundamental
    return {
        "signal": plot.variables[index].name,
        "fundamental_hz": fundamental_hz,
        "thd": ratio,
        "thd_percent": ratio * 100.0,
    }


def fft_spectrum(plot: RawPlot, name: str) -> tuple[list[float], list[float]]:
    """Return frequency and magnitude arrays for one real trace."""

    index = find_signal(plot, name)
    time = plot.real[:, 0]
    values = np.real(column_complex(plot, index))
    centered = values - np.mean(values)
    spectrum = np.abs(np.fft.rfft(centered))
    freqs = np.fft.rfftfreq(len(centered), d=float(np.mean(np.diff(time))))
    return [float(value) for value in freqs], [float(value) for value in spectrum]


def split_steps(plot: RawPlot) -> list[tuple[int, int]]:
    """Split a plot where the x axis restarts."""

    x_values = plot.real[:, 0]
    spans: list[tuple[int, int]] = []
    start = 0
    for index in range(1, len(x_values)):
        if x_values[index] < x_values[index - 1]:
            spans.append((start, index))
            start = index
    spans.append((start, len(x_values)))
    return spans
