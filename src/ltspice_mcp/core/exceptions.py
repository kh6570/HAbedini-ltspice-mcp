# In the name of God, the Most Gracious, the Most Merciful
"""Domain exceptions. All user-facing errors derive from LTspiceError."""

from __future__ import annotations

from mcp_app_core.errors import AppError

from ltspice_mcp.core.error_taxonomy import DEFAULT_ERROR_CODE


class LTspiceError(AppError):
    """Base exception for all ltspice-mcp errors."""

    default_error_code = DEFAULT_ERROR_CODE


class AdapterNotFoundError(LTspiceError):
    """No adapter registered that can handle the requested simulator."""

    default_error_code = "backend_unavailable"


class BackendUnavailableError(LTspiceError):
    """A required local backend or the LTspice executable is unavailable."""

    default_error_code = "backend_unavailable"


class ArtifactMissingError(LTspiceError):
    """A requested or expected artifact could not be found or was not created."""

    default_error_code = "artifact_missing"


class BatchConflictError(LTspiceError):
    """The requested retained-batch action conflicts with persisted state."""

    default_error_code = "batch_conflict"


class SimulationError(LTspiceError):
    """LTspice failed to complete a simulation."""

    default_error_code = "simulation_failed"

    def __init__(
        self,
        message: str,
        *,
        exit_code: int | None = None,
        stderr: str | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(message, error_code=error_code)
        self.exit_code = exit_code
        self.stderr = stderr


class ConvergenceError(SimulationError):
    """Simulator failed to converge."""

    default_error_code = "convergence_failed"


class ParseError(LTspiceError):
    """Failed to parse a schematic, netlist, log, or raw file."""

    default_error_code = "parse_failed"

    def __init__(
        self,
        message: str,
        *,
        line: int | None = None,
        column: int | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(message, error_code=error_code)
        self.line = line
        self.column = column


class SchematicInvalidError(ParseError):
    """The schematic structure is invalid for the requested operation."""

    default_error_code = "schematic_invalid"


class BudgetExceededError(LTspiceError):
    """A DataBudget was exceeded and no downsampling strategy could satisfy it."""

    default_error_code = "budget_exceeded"


class SandboxViolationError(LTspiceError):
    """Attempted file access outside the sandbox root."""

    default_error_code = "sandbox_violation"


class ValidationError(LTspiceError, ValueError):
    """Caller-supplied input failed a validation precondition."""

    default_error_code = "validation_failed"


class UnsupportedManifestVersionError(ValidationError):
    """A persisted artifact uses a schema version this server cannot load."""

    default_error_code = "unsupported_manifest_version"


class ConfigurationError(LTspiceError):
    """Runtime configuration is missing or invalid."""

    default_error_code = "configuration_invalid"


class SimulationTimeoutError(SimulationError):
    """Simulation exceeded its timeout."""

    default_error_code = "timeout_exceeded"


class UnsupportedError(LTspiceError):
    """The requested capability has no LTspice equivalent."""

    default_error_code = "unsupported"
