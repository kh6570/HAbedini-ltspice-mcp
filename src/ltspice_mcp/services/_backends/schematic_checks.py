# In the name of God, the Most Gracious, the Most Merciful
"""Structural checks for schematics and netlists."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp_app_core.checks import CheckFinding, CheckResult

from ltspice_mcp.services._backends.asc_geometry import connect_nets, symbol_pins

if TYPE_CHECKING:
    from ltspice_mcp.services._backends.asc_document import Schematic

CHECK_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "ok": {"type": "boolean"},
        "error_count": {"type": "integer"},
        "warning_count": {"type": "integer"},
        "info_count": {"type": "integer"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["severity", "code", "message", "fixable"],
                "properties": {
                    "severity": {"type": "string"},
                    "code": {"type": "string"},
                    "message": {"type": "string"},
                    "fixable": {
                        "type": "boolean",
                        "description": "True when a later edit tool can repair this finding.",
                    },
                    "location": {
                        "type": "string",
                        "description": "Reference designator, pin, wire, or line number.",
                    },
                },
            },
        },
    },
}

_ANALYSES = frozenset({"tran", "ac", "dc", "op", "noise", "tf"})
_NETLIST_ANALYSES = frozenset({".tran", ".ac", ".dc", ".op", ".noise", ".tf"})


def schematic_findings(schematic: Schematic) -> tuple[CheckFinding, ...]:
    """Return structural findings for one schematic."""

    findings: list[CheckFinding] = []
    if not any(flag.name == "0" for flag in schematic.flags()):
        findings.append(
            CheckFinding(
                severity="error",
                code="missing_ground",
                message="No ground flag (FLAG ... 0).",
                fixable=True,
                location="schematic",
            )
        )
    commands = {item.command() for item in schematic.texts() if item.is_directive}
    if not commands.intersection(_ANALYSES):
        findings.append(
            CheckFinding(
                severity="error",
                code="missing_analysis",
                message="No analysis directive (.tran, .ac, .dc, .op, .noise, or .tf).",
                fixable=True,
                location="directives",
            )
        )
    seen: set[str] = set()
    for symbol in schematic.symbols():
        reference = symbol.reference()
        place = f"{symbol.name} {symbol.x},{symbol.y}"
        if not reference:
            findings.append(
                CheckFinding(
                    severity="error",
                    code="missing_reference",
                    message=f"Symbol {symbol.name} has no InstName.",
                    fixable=False,
                    location=place,
                )
            )
        elif reference in seen:
            findings.append(
                CheckFinding(
                    severity="error",
                    code="duplicate_reference",
                    message=f"Duplicate reference {reference}.",
                    fixable=True,
                    location=reference,
                )
            )
        if reference:
            seen.add(reference)
    for wire in schematic.wires():
        if wire.x1 != wire.x2 and wire.y1 != wire.y2:
            findings.append(
                CheckFinding(
                    severity="error",
                    code="diagonal_wire",
                    message=f"{wire.emit()} is diagonal.",
                    fixable=True,
                    location=f"{wire.x1},{wire.y1},{wire.x2},{wire.y2}",
                )
            )
    nets = connect_nets(schematic)
    for symbol in schematic.symbols():
        label = symbol.reference() or symbol.name
        for pin in symbol_pins(symbol):
            if (pin.x, pin.y) not in nets:
                findings.append(
                    CheckFinding(
                        severity="error",
                        code="floating_pin",
                        message=f"{label} pin {pin.name} is not on a wire or flag.",
                        fixable=True,
                        location=f"{label} pin {pin.name}",
                    )
                )
    return tuple(findings)


def netlist_findings(text: str) -> tuple[CheckFinding, ...]:
    """Return structural findings for one netlist."""

    findings: list[CheckFinding] = []
    seen: set[str] = set()
    has_ground = False
    has_analysis = False
    for number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("*"):
            continue
        if line.startswith("."):
            command = line.split(maxsplit=1)[0].lower()
            if command in _NETLIST_ANALYSES:
                has_analysis = True
            continue
        parts = line.split()
        name = parts[0]
        location = f"line {number}"
        if name in seen:
            findings.append(
                CheckFinding(
                    severity="error",
                    code="duplicate_reference",
                    message=f"Duplicate reference {name}.",
                    fixable=True,
                    location=location,
                )
            )
        else:
            seen.add(name)
        if "0" in parts[1:]:
            has_ground = True
    if not has_ground:
        findings.append(
            CheckFinding(
                severity="error",
                code="missing_ground",
                message="No component connects to node 0.",
                fixable=True,
                location="netlist",
            )
        )
    if not has_analysis:
        findings.append(
            CheckFinding(
                severity="error",
                code="missing_analysis",
                message="No analysis directive (.tran, .ac, .dc, .op, .noise, or .tf).",
                fixable=True,
                location="netlist",
            )
        )
    return tuple(findings)


def check_payload(findings: tuple[CheckFinding, ...]) -> dict[str, object]:
    """Return the JSON check result, including location and fixable."""

    return CheckResult(findings=findings, output_schema=CHECK_OUTPUT_SCHEMA).as_dict()


def introduced_findings(
    previous: tuple[CheckFinding, ...],
    current: tuple[CheckFinding, ...],
) -> tuple[CheckFinding, ...]:
    """Return findings in ``current`` that were not already in ``previous``."""

    seen = {(item.code, item.location, item.message) for item in previous}
    return tuple(item for item in current if (item.code, item.location, item.message) not in seen)
