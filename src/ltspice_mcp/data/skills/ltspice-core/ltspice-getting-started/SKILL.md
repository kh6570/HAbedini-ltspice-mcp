---
name: ltspice-getting-started
description: Start an LTspice MCP task. Use this skill to edit an .asc, to run a batch simulation, or to decide which procedure skill to open.
license: MIT
metadata:
  author: ltspice-mcp
  version: "1.0"
---
In the name of God, the Most Gracious, the Most Merciful

# LTspice: Start

The `.asc` schematic is the source of truth. LTspice produces `.net`, `.log`, and `.raw`. A batch run netlists the schematic, then simulates that netlist.

## When to use

Use this when you start an LTspice task and you are unsure which tool to call.

## When not to use

Do not use this for the numbered measure steps or for convergence repair.
Those optional skills are `ltspice-run-and-measure` and
`ltspice-debug-convergence`. These skills do not load automatically.

## Reference files

- `batch-contract.md` — how you launch a batch run
