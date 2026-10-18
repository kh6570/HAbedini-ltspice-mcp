# In the name of God, the Most Gracious, the Most Merciful
"""Size budgets. Limits are implemented in mcp-app-core."""

from __future__ import annotations

from mcp_app_core.budgets import DataBudget as _CoreBudget
from mcp_app_core.budgets import DownsampleStrategy
from mcp_app_core.budgets import downsample_indices as _downsample_indices
from mcp_app_core.errors import BudgetExceededError as _CoreBudgetExceeded
from mcp_app_core.errors import ValidationError as _CoreValidationError

from ltspice_mcp.core.exceptions import BudgetExceededError, ValidationError

__all__ = ["DEFAULT_BUDGET", "DataBudget", "DownsampleStrategy", "downsample_indices"]


class DataBudget(_CoreBudget):
    """Server budget that raises LTspice validation errors."""

    def __post_init__(self) -> None:
        try:
            super().__post_init__()
        except _CoreValidationError as exc:
            raise ValidationError(str(exc)) from exc


DEFAULT_BUDGET = DataBudget()


def downsample_indices(n_points: int, target: int) -> list[int]:
    """Downsample and raise the LTspice budget error."""

    try:
        return _downsample_indices(n_points, target)
    except _CoreBudgetExceeded as exc:
        raise BudgetExceededError(str(exc)) from exc
