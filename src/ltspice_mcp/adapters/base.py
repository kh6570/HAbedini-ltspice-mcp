# In the name of God, the Most Gracious, the Most Merciful
"""Adapter descriptions for the LTspice command line."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class AdapterCapabilities:
    """What one LTspice adapter can do."""

    netlist: bool = True
    batch_simulation: bool = True
    ascii_raw: bool = True
    private_ini: bool = False


@dataclass(frozen=True, slots=True)
class AdapterDescription:
    """Identity of one simulator adapter."""

    key: str
    title: str
    summary: str
    capabilities: AdapterCapabilities = field(default_factory=AdapterCapabilities)


@dataclass(frozen=True, slots=True)
class SimulationCommand:
    """One ready-to-run LTspice command."""

    argv: tuple[str, ...]
    cwd: Path
    log_path: Path
    raw_path: Path | None
    netlist_path: Path | None
