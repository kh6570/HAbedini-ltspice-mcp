---
name: ltspice-getting-started
description: Start an LTspice MCP task. Use when editing an .asc, running a batch simulation, or deciding which procedure skill to open.
license: MIT
metadata:
  author: ltspice-mcp
  version: "1.0"
---
In the name of God, the Most Gracious, the Most Merciful

# LTspice: Getting Started

The `.asc` schematic is the source of truth. `.net`, `.log`, and `.raw` are
produced by LTspice. A batch run netlists the schematic, then simulates that
netlist.

## When to use

Use this when starting an LTspice task and you are unsure which tool to call.

## When not to use

Do not use this for the numbered measure steps or for convergence repair.
Those optional skills are `ltspice-run-and-measure` and
`ltspice-debug-convergence`. They are not auto-loaded.

## Reference files

- `batch-contract.md` — how a batch run is launched
