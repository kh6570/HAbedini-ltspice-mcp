# In the name of God, the Most Gracious, the Most Merciful
"""LTspice MCP package.

Public re-exports stay narrow: the base error type and the package version.
"""

from __future__ import annotations

from ltspice_mcp.core.exceptions import LTspiceError

__all__ = [
    "LTspiceError",
    "__version__",
]

__version__ = "0.0.1"
