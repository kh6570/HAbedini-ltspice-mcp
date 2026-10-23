In the name of God, the Most Gracious, the Most Merciful

# User guide

## What this server does

`ltspice-mcp` lets an assistant edit `.asc` schematics, run LTspice, and read logs and waveforms. The schematic is the source of truth. `.net`, `.log`, and `.raw` are produced by LTspice.

Waveform tools return at most 2000 points. Ask for a plot, a CSV export, or a `.meas` result when the trace is larger.

## Requirements

- Windows
- Python 3.11 or newer
- LTspice XVII (`XVIIx64.exe`) or a later install (`LTspice.exe`)

This tree was checked against LTspice XVII 17.0.37 at `C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe`.

## Install

This server depends on `mcp-app-core`. `pip install` clones it from GitHub. You do not clone that repository yourself.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Or run `scripts\setup_mcp.ps1`, which installs the core, creates the venv, and merges an `ltspice-mcp` entry into the Cursor and VS Code user MCP configs. The name is `ltspice-mcp` so it does not collide with Analog's installer entry. It leaves any existing `qspice` server in place.

## Run

```powershell
.\.venv\Scripts\ltspice-mcp.exe --describe
.\.venv\Scripts\ltspice-mcp.exe --setup
```

Useful flags:

| Flag | Environment variable |
| --- | --- |
| `--ltspice-exe` | `LTSPICE_EXE` |
| `--workspace-root` | `LTSPICE_WORKSPACE_ROOT` |
| `--log-level` | `LTSPICE_LOG_LEVEL` |
| `--active-profiles` | `LTSPICE_ACTIVE_PROFILES` |
| `--window-sync` | `LTSPICE_WINDOW_SYNC` |

The timeout is `LTSPICE_TIMEOUT_S` (default 120 seconds). Set it to `0` to disable the limit.

The server probes, in order: `LTSPICE_EXE`, `Program Files\LTC\LTspiceXVII\XVIIx64.exe`, `Program Files\ADI\LTspice\LTspice.exe`, then the per-user ADI install. It reads the version from the executable and looks for `ltspice-mcp-bridge.exe` beside it. It does not launch the GUI to ask for a version.

A normal session omits remote, batch, live GUI, and topology ingest. Set `LTSPICE_ACTIVE_PROFILES=default,extended` to load them. `describe_server_capabilities` lists the hidden groups.

Existing schematic edits need `expected_hash` from the previous read. LTspice XVII stays launch-only. On 26.1 or newer, `LTSPICE_WINDOW_SYNC=1` attaches a save to a schematic you already have open and pushes the new text as one undo step. It does not start a hidden LTspice.

## Documentation

| Doc | Purpose |
| --- | --- |
| [Tool reference](tool_reference.md) | Every tool and its required arguments |
| [Architecture](architecture.md) | How a schematic becomes a simulation |
| [Error codes](errors.md) | Stable codes on tool failures |
| [Security](security.md) | What the sandbox does |

## A simulation

1. `create_starter_schematic` or `create_schematic` plus `add_component`.
2. `prepare_transient` or another prepare tool. Directives are `!.tran` text on the schematic.
3. `run_simulation`. An `.asc` is netlisted with `-netlist`, then the `.net` is run with `-b -ascii`.
4. `read_measures` for `.meas` lines in the `.log`.
5. `read_waveform` for a trace in the `.raw` file.

`-b` on an `.asc` opens the LTspice window and does not return, so the server never does that. `-ini` also hangs XVII 17.0.37, so batch runs use the normal user profile.

## What LTspice does not have

- No C++ DLL, Verilog, or socket custom devices. Use a `.asy` symbol, a hierarchical block, or a behavioral source.
- No GUI command channel. `open_schematic_in_gui` launches LTspice. Poll and command tools return `unsupported`.

## Encoding

`.asc` and `.asy` files are Windows-1252. The editor reads and writes them as Latin-1 so a micro sign already in a file survives. New values use `u`, not `µ`. `1M` is milli. Mega is `Meg`.
