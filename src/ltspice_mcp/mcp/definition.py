# In the name of God, the Most Gracious, the Most Merciful
"""Server metadata used by the MCP bootstrap layer."""

from __future__ import annotations

from dataclasses import dataclass

from ltspice_mcp.infra.config import LTspiceFeatures


@dataclass(frozen=True, slots=True)
class ServerParameter:
    """A user-configurable server parameter."""

    name: str
    description: str
    env_var: str | None = None
    required: bool = False


@dataclass(frozen=True, slots=True)
class ServerDefinition:
    """Top-level description of the LTspice MCP server."""

    name: str
    title: str
    instructions: str
    features: LTspiceFeatures
    parameters: tuple[ServerParameter, ...]


def build_server_definition(features: LTspiceFeatures | None = None) -> ServerDefinition:
    """Return the current server definition."""

    return ServerDefinition(
        name="ltspice-mcp",
        title="LTspice MCP Server",
        instructions=(
            "Treat .asc files as the source of truth, keep netlists and waveform "
            "artifacts derived, and prefer bounded signal summaries over raw dumps. "
            "LTspice has no C++ DLL custom devices and no GUI command channel."
        ),
        features=features or LTspiceFeatures(),
        parameters=(
            ServerParameter(
                name="ltspice-exe",
                description="Absolute path to XVIIx64.exe or LTspice.exe.",
                env_var="LTSPICE_EXE",
            ),
            ServerParameter(
                name="workspace-root",
                description="Workspace root used to sandbox file access.",
                env_var="LTSPICE_WORKSPACE_ROOT",
            ),
            ServerParameter(
                name="log-level",
                description="Minimum structured log level.",
                env_var="LTSPICE_LOG_LEVEL",
            ),
        ),
    )
