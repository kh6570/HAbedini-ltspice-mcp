# In the name of God, the Most Gracious, the Most Merciful
"""Pure domain types for ltspice-mcp."""

from __future__ import annotations

from ltspice_mcp.core.budgets import DEFAULT_BUDGET, DataBudget
from ltspice_mcp.core.exceptions import LTspiceError

__all__ = ["DEFAULT_BUDGET", "DataBudget", "LTspiceError"]
