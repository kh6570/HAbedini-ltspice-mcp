---
name: ltspice-run-and-measure
description: Run an LTspice schematic. Read a bounded measurement. Use when you already have the drawn circuit and you need a .meas result or a short waveform trace.
license: MIT
metadata:
  author: ltspice-mcp
  version: "1.0"
---
In the name of God, the Most Gracious, the Most Merciful

# LTspice: Run and Measure

Keep the `.asc` file as the source of truth. Add one analysis. Run it. Read the number from the log before you ask for a trace.

## When to use

Use this when the schematic already exists and the task is to simulate it and
report a measurement.

## When not to use

Do not use this to debug a convergence failure. Open
`ltspice-debug-convergence` when the log shows a timestep or singular-matrix
failure.

## Reference files

- `workflow.md` — analysis directive, `.meas`, run, and bounded waveform read
