# In the name of God, the Most Gracious, the Most Merciful
"""Size budgets. mcp-app-core implements the limits."""

from __future__ import annotations

from mcp_app_core.budgets import DataBudget as _CoreBudget
from mcp_app_core.errors import ValidationError as _CoreValidationError

from ltspice_mcp.core.exceptions import ValidationError

__all__ = ["DEFAULT_BUDGET", "DataBudget"]


class DataBudget(_CoreBudget):
    """Server budget that raises LTspice validation errors."""

    def __post_init__(self) -> None:
        try:
            super().__post_init__()
        except _CoreValidationError as exc:
            raise ValidationError(str(exc)) from exc


DEFAULT_BUDGET = DataBudget()
