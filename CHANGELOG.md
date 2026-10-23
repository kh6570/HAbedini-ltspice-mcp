In the name of God, the Most Gracious, the Most Merciful

# Changelog

## Unreleased

- Default sessions hide remote, batch, live GUI, and topology ingest. `describe_server_capabilities` lists those groups and how to enable them.
- Schematic saves require the content hash from the last read. A mismatch writes nothing.
- `plot_waveforms` and `render_schematic_image` return a PNG in the tool result. Waveform downsampling uses minmax.
- `check_schematic` and `check_netlist` include location and whether a later edit can fix the finding.
- LTspice 26.1 reports `ltspice-mcp-bridge.exe` when it sits beside `LTspice.exe`. Window sync is opt-in and attaches only to a window the user already opened.
- A batch run counts as success only when a new log is newer than the process start and contains `Total elapsed time`.
- The setup script registers the server as `ltspice-mcp`.
- Workflow notes `run-and-measure` and `debug-convergence` are short routers. The steps live in optional skills under `data/skills/` and are not returned by `read_workflow_instruction`.

## 0.0.1

- First LTspice MCP server: `.asc` editor, LTspice XVII batch runs, waveform and `.meas` reads.
- Depends on `mcp-app-core`. `pip install` clones https://github.com/kh6570/HAbedini-mcp-app-core.
- No DLL, Verilog, or socket devices. Symbols, hierarchical blocks, and behavioral sources are the mixed-signal surface.
- Opening a schematic in the GUI is supported. A GUI command channel is not.
