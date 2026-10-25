In the name of God, the Most Gracious, the Most Merciful

# LTspice agent skills

Skills are client-side routers. The MCP server does not load them. `read_workflow_instruction` returns the short note in `data/instructions/`, not the reference procedure.

| Group | Install | Skills |
| --- | --- | --- |
| `ltspice-core` | default orientation | `ltspice-getting-started` |
| `ltspice-procedures` | optional, does not load automatically | `ltspice-run-and-measure`, `ltspice-debug-convergence` |

Copy a skill directory into the agent skills folder only when that task needs it. There is no installer, and the server never reads `reference/*.md` on its own.
