---
name: ltspice-debug-convergence
description: Debug an LTspice simulation that fails to converge. Use when the log reports timestep too small, a singular matrix, or the run stops early.
license: MIT
metadata:
  author: ltspice-mcp
  version: "1.0"
---
In the name of God, the Most Gracious, the Most Merciful

# LTspice: Debug Convergence

A convergence failure is a circuit or numeric problem. Read the log, then
change one thing.

## When to use

Use this when a run does not finish, or the log names a timestep or singular
matrix problem.

## When not to use

Do not use this after a run that already finished, and do not use it to draw
a new schematic. Open `ltspice-run-and-measure` for a measurement.

## Reference files

- `workflow.md` — ground path, options, and how to tell a warning from a failure
