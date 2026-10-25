In the name of God, the Most Gracious, the Most Merciful

# Architecture

`ltspice-mcp` is a local MCP server. The assistant calls tools. The server edits `.asc` files and starts `XVIIx64.exe` or `LTspice.exe` as a short-lived process. Paths must stay inside `--workspace-root`.

```mermaid
flowchart LR
    AI["AI client"] --> MCP["ltspice-mcp"]
    MCP --> EXE["LTspice -netlist and -b"]
    MCP --> WS["Workspace .asc .net .log .raw"]
    EXE --> WS
```

## Layers

The catalog, workspace sandbox, data budget, error base, and settings base come from the package `mcp-app-core`. `pip install` of this server clones that package from GitHub. This repository keeps the LTspice-specific pieces:

- `core` publishes `LTspiceError` (a subclass of the shared `AppError`) and the LTspice error-code list.
- `infra` loads `LTSPICE_*` settings and runs subprocesses through the shared timeout helper.
- `adapters` find the executable and build `-netlist` and `-b -ascii` commands. The adapters classify the log text after the process exits. Success is the line `Total elapsed time`.
- `services` own the `.asc` editor, the clean-room netlist, the `.raw` reader, and one module per tool.
- `mcp` registers those tools with FastMCP. It does not parse schematics.

A tool is a module under `services/<group>/` with a `SERVICE_SPEC`, plus a row in that group's `mcp_contracts.py`. The catalog discovers both.

## Simulation

1. If the source is an `.asc`, `XVIIx64.exe -netlist file.asc` writes `file.net`.
2. `XVIIx64.exe -b -ascii file.net` writes `file.log` and `file.raw`.
3. The raw reader accepts ASCII `Values:` data, uncompressed `Binary:` data, and LTspice compressed real data.
4. The server reads `.meas` results from the log.

Unit tests use the clean-room netlist when LTspice is absent. The tests check a divider without the executable. The clean-room netlist covers the built-in primitives only.

## Batch and the GUI

`-b` applied directly to an `.asc` opens the schematic window. `-ini` with XVII 17.0.37 does not return. The adapter avoids both.

`open_schematic_in_gui` starts LTspice on an `.asc` with no `-b`. The server has no channel for commands back from that window.
