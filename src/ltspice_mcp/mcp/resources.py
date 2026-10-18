# In the name of God, the Most Gracious, the Most Merciful
"""Static guideline resources."""

from __future__ import annotations

from dataclasses import dataclass

_RESOURCES: dict[str, str] = {
    "guidelines://ltspice-artifacts": (
        "The .asc schematic is the source of truth. "
        ".net, .log, and .raw files are derived by LTspice. "
        "Batch runs use -b and -ascii so the raw file stays text. "
        "A private -ini file keeps the run from rewriting the user profile."
    ),
    "guidelines://ltspice-measurements": (
        ".meas results are printed in the .log. "
        "There is no separate measurement executable. "
        "Read them with read_measures. Waveform reads are capped at 2000 points."
    ),
}


@dataclass(frozen=True, slots=True)
class ResourceDefinition:
    """One static MCP resource."""

    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


def get_resource_definitions() -> tuple[ResourceDefinition, ...]:
    """Return the static resources."""

    return tuple(
        ResourceDefinition(uri=uri, name=uri.rsplit("/", maxsplit=1)[-1], description=text[:80])
        for uri, text in _RESOURCES.items()
    )


def get_resource_content(uri: str) -> str | None:
    """Return one resource body."""

    return _RESOURCES.get(uri)
