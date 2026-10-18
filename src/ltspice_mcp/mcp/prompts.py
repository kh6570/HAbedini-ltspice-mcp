# In the name of God, the Most Gracious, the Most Merciful
"""Prompt templates for common LTspice tasks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PromptDefinition:
    """One MCP prompt."""

    name: str
    description: str
    body: str


def get_prompt_definitions() -> tuple[PromptDefinition, ...]:
    """Return the bundled prompts."""

    return (
        PromptDefinition(
            name="ltspice_divider_from_scratch",
            description="Author a resistive divider and check the midpoint voltage.",
            body=(
                "Create a divider schematic, run a transient analysis, and confirm "
                "that V(out) is about half of the source."
            ),
        ),
        PromptDefinition(
            name="ltspice_run_and_measure",
            description="Run a schematic and read a .meas result.",
            body="Add .tran and .meas, run_simulation, then read_measures from the log.",
        ),
        PromptDefinition(
            name="ltspice_debug_convergence",
            description="Inspect a failed LTspice log.",
            body=(
                "Read the log. Check for a ground flag, a single analysis directive, "
                "and timestep or singular-matrix messages."
            ),
        ),
    )
