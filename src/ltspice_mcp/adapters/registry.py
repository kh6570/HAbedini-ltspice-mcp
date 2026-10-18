# In the name of God, the Most Gracious, the Most Merciful
"""Select the LTspice CLI adapter for a probed executable."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ltspice_mcp.adapters.cli.ltspice_v1 import LtspiceCliV1, describe_ltspice_v1
from ltspice_mcp.core.exceptions import AdapterNotFoundError

if TYPE_CHECKING:
    from ltspice_mcp.adapters.base import AdapterDescription
    from ltspice_mcp.adapters.probe import ProbeResult


def describe_adapters(probe: ProbeResult) -> tuple[AdapterDescription, ...]:
    """Return the adapters that could serve this probe result."""

    if not probe.exists:
        return ()
    return (describe_ltspice_v1(probe),)


def select_adapter(probe: ProbeResult) -> type[LtspiceCliV1]:
    """Return the adapter class for a probed LTspice executable."""

    if probe.executable is None or not probe.exists:
        raise AdapterNotFoundError("LTspice is not available.")
    return LtspiceCliV1
