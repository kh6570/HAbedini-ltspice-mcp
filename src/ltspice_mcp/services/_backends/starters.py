# In the name of God, the Most Gracious, the Most Merciful
"""Original starter schematics used by recipes and layout specs.

These circuits are authored for this project. They are not Analog Devices examples.
"""

from __future__ import annotations

from ltspice_mcp.services._backends.asc_document import Schematic, blank_schematic
from ltspice_mcp.services._backends.asc_edit import (
    add_net_label,
    add_primitive,
    add_wire,
    upsert_directive,
)


def _base(version: str) -> Schematic:
    schematic = blank_schematic(version=version)
    schematic.width = 880
    schematic.height = 680
    return schematic


def build_divider(version: str = "Version 4") -> Schematic:
    """10 V source, two 1 k resistors, output taken at the midpoint."""

    schematic = _base(version)
    add_primitive(
        schematic, kind="voltage_source", reference="V1", value="10", x=48, y=80, rotation="R0"
    )
    add_primitive(
        schematic, kind="resistor", reference="R1", value="1k", x=144, y=80, rotation="R0"
    )
    add_primitive(
        schematic, kind="resistor", reference="R2", value="1k", x=144, y=160, rotation="R0"
    )
    add_wire(schematic, x1=48, y1=96, x2=160, y2=96)
    add_wire(schematic, x1=48, y1=176, x2=48, y2=256)
    add_wire(schematic, x1=48, y1=256, x2=160, y2=256)
    add_net_label(schematic, x=48, y=96, name="in")
    add_net_label(schematic, x=160, y=176, name="out")
    add_net_label(schematic, x=160, y=256, name="0")
    upsert_directive(schematic, ".tran 1m")
    upsert_directive(schematic, ".meas TRAN vout AVG V(out)")
    return schematic


def build_rc(version: str = "Version 4") -> Schematic:
    """Series R and shunt C driven by a pulse, a first-order low-pass."""

    schematic = _base(version)
    add_primitive(
        schematic,
        kind="voltage_source",
        reference="V1",
        value="PULSE(0 1 0 1u 1u 0.5m 1m)",
        x=48,
        y=80,
        rotation="R0",
    )
    add_primitive(
        schematic, kind="resistor", reference="R1", value="1k", x=144, y=80, rotation="R0"
    )
    add_primitive(
        schematic, kind="capacitor", reference="C1", value="1u", x=144, y=176, rotation="R0"
    )
    add_wire(schematic, x1=48, y1=96, x2=160, y2=96)
    add_wire(schematic, x1=48, y1=176, x2=48, y2=272)
    add_wire(schematic, x1=48, y1=272, x2=160, y2=272)
    add_wire(schematic, x1=160, y1=240, x2=160, y2=272)
    add_net_label(schematic, x=160, y=176, name="out")
    add_net_label(schematic, x=160, y=272, name="0")
    upsert_directive(schematic, ".tran 5m")
    upsert_directive(schematic, ".meas TRAN vout AVG V(out)")
    return schematic


def build_buck(version: str = "Version 4") -> Schematic:
    """Open-loop buck power stage switched by a pulsed voltage and a diode."""

    schematic = _base(version)
    schematic.width = 1200
    schematic.height = 880
    add_primitive(
        schematic,
        kind="voltage_source",
        reference="V1",
        value="PULSE(0 12 0 10n 10n 5u 10u)",
        x=64,
        y=64,
        rotation="R0",
    )
    add_primitive(
        schematic, kind="inductor", reference="L1", value="10u", x=240, y=48, rotation="R0"
    )
    add_primitive(schematic, kind="diode", reference="D1", value="D", x=176, y=160, rotation="R180")
    add_primitive(
        schematic, kind="capacitor", reference="C1", value="100u", x=400, y=160, rotation="R0"
    )
    add_primitive(
        schematic, kind="resistor", reference="R1", value="5", x=528, y=160, rotation="R0"
    )
    add_wire(schematic, x1=64, y1=80, x2=256, y2=80)
    add_wire(schematic, x1=256, y1=144, x2=416, y2=144)
    add_wire(schematic, x1=416, y1=144, x2=544, y2=144)
    add_wire(schematic, x1=64, y1=160, x2=64, y2=320)
    add_wire(schematic, x1=64, y1=320, x2=544, y2=320)
    add_net_label(schematic, x=416, y=144, name="out")
    add_net_label(schematic, x=544, y=320, name="0")
    upsert_directive(schematic, ".model D D")
    upsert_directive(schematic, ".tran 2m")
    upsert_directive(schematic, ".meas TRAN vout AVG V(out)")
    return schematic


def build_named(name: str, version: str = "Version 4") -> Schematic:
    """Return one of the built-in starter schematics."""

    key = name.strip().lower()
    if key in {"divider", "resistive_divider"}:
        return build_divider(version)
    if key in {"rc", "rc_lowpass"}:
        return build_rc(version)
    if key in {"buck", "buck_behavioral"}:
        return build_buck(version)
    return build_divider(version)
