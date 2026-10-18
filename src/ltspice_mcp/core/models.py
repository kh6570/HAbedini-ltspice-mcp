# In the name of God, the Most Gracious, the Most Merciful
"""Simulator-neutral value objects shared by services."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TraceSeries:
    """One waveform trace, real or complex, already loaded into memory."""

    name: str
    x_name: str
    x: tuple[float, ...]
    real: tuple[float, ...]
    imag: tuple[float, ...] | None = None

    @property
    def complex_data(self) -> bool:
        """Return True when the trace carries an imaginary part."""

        return self.imag is not None
