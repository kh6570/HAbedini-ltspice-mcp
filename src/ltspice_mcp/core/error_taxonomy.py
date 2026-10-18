# In the name of God, the Most Gracious, the Most Merciful
"""Published stable error-code taxonomy for MCP clients."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DEFAULT_ERROR_CODE = "ltspice_error"
ERRORS_DOCUMENT_PATH = "docs/errors.md"

ErrorCodeStatus = Literal["implemented", "reserved"]


@dataclass(frozen=True, slots=True)
class ErrorCodeDefinition:
    """One published error code and its current implementation status."""

    code: str
    title: str
    summary: str
    status: ErrorCodeStatus
    mapped_exceptions: tuple[str, ...] = ()

    def summary_dict(self) -> dict[str, object]:
        """Return a JSON-serializable summary for capability reporting."""

        return {
            "code": self.code,
            "title": self.title,
            "summary": self.summary,
            "status": self.status,
            "mapped_exceptions": list(self.mapped_exceptions),
        }


ERROR_CODE_DEFINITIONS: tuple[ErrorCodeDefinition, ...] = (
    ErrorCodeDefinition(
        code=DEFAULT_ERROR_CODE,
        title="Generic LTspice Error",
        summary="Fallback code for domain failures without a more specific stable code.",
        status="implemented",
        mapped_exceptions=("LTspiceError",),
    ),
    ErrorCodeDefinition(
        code="backend_unavailable",
        title="Backend Unavailable",
        summary="The LTspice executable or a required local backend is unavailable.",
        status="implemented",
        mapped_exceptions=("AdapterNotFoundError", "BackendUnavailableError"),
    ),
    ErrorCodeDefinition(
        code="artifact_missing",
        title="Artifact Missing",
        summary="A requested or expected derived artifact was not created or could not be found.",
        status="implemented",
        mapped_exceptions=("ArtifactMissingError",),
    ),
    ErrorCodeDefinition(
        code="schematic_invalid",
        title="Schematic Invalid",
        summary="The schematic structure is invalid or incomplete for the requested operation.",
        status="implemented",
        mapped_exceptions=("SchematicInvalidError",),
    ),
    ErrorCodeDefinition(
        code="batch_conflict",
        title="Batch Conflict",
        summary="The requested batch action conflicts with persisted batch state.",
        status="implemented",
        mapped_exceptions=("BatchConflictError",),
    ),
    ErrorCodeDefinition(
        code="timeout_exceeded",
        title="Timeout Exceeded",
        summary="The simulation exceeded its configured timeout.",
        status="implemented",
        mapped_exceptions=("SimulationTimeoutError",),
    ),
    ErrorCodeDefinition(
        code="simulation_failed",
        title="Simulation Failed",
        summary="LTspice completed unsuccessfully.",
        status="implemented",
        mapped_exceptions=("SimulationError",),
    ),
    ErrorCodeDefinition(
        code="convergence_failed",
        title="Convergence Failed",
        summary="LTspice failed to converge on the requested analysis.",
        status="implemented",
        mapped_exceptions=("ConvergenceError",),
    ),
    ErrorCodeDefinition(
        code="parse_failed",
        title="Parse Failed",
        summary="A schematic, netlist, waveform, or log could not be parsed.",
        status="implemented",
        mapped_exceptions=("ParseError",),
    ),
    ErrorCodeDefinition(
        code="budget_exceeded",
        title="Budget Exceeded",
        summary="Waveform size limits could not be satisfied even after downsampling.",
        status="implemented",
        mapped_exceptions=("BudgetExceededError",),
    ),
    ErrorCodeDefinition(
        code="sandbox_violation",
        title="Sandbox Violation",
        summary="A requested filesystem path escaped the configured workspace sandbox.",
        status="implemented",
        mapped_exceptions=("SandboxViolationError",),
    ),
    ErrorCodeDefinition(
        code="validation_failed",
        title="Validation Failed",
        summary="Caller input failed a validation precondition.",
        status="implemented",
        mapped_exceptions=("ValidationError",),
    ),
    ErrorCodeDefinition(
        code="configuration_invalid",
        title="Configuration Invalid",
        summary="Runtime configuration is missing or invalid.",
        status="implemented",
        mapped_exceptions=("ConfigurationError",),
    ),
    ErrorCodeDefinition(
        code="unsupported",
        title="Unsupported",
        summary="LTspice has no equivalent for the requested operation.",
        status="implemented",
        mapped_exceptions=("UnsupportedError",),
    ),
    ErrorCodeDefinition(
        code="unsupported_manifest_version",
        title="Unsupported Manifest Version",
        summary="A persisted artifact uses a schema version this server cannot load.",
        status="implemented",
        mapped_exceptions=("UnsupportedManifestVersionError",),
    ),
)


def error_code_catalog() -> list[dict[str, object]]:
    """Return the published error-code catalog."""

    return [item.summary_dict() for item in ERROR_CODE_DEFINITIONS]
