In the name of God, the Most Gracious, the Most Merciful

# LTspice MCP

A [Model Context Protocol](https://modelcontextprotocol.io) server for [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html). An assistant can edit `.asc` schematics, run the simulator, and read logs and waveforms through stable JSON tools.

The `.asc` file is the source of truth. `.net`, `.log`, and `.raw` are produced by LTspice. Waveform reads stay inside a 2000-point budget.

The shared server framework is the Python package `mcp-app-core`. `pip install` of this server clones it from GitHub. This repository contains the LTspice editor, command line, and tools.

## Requirements

- Windows
- Python 3.11 or newer
- LTspice XVII (`XVIIx64.exe`) or a later install (`LTspice.exe`)

## Install

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

`pip install` clones [mcp-app-core](https://github.com/kh6570/HAbedini-mcp-app-core). You do not clone that repository yourself.

```powershell
.\.venv\Scripts\ltspice-mcp.exe --describe
```

To register the server in Cursor and VS Code without removing an existing `qspice` entry:

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\setup_mcp.ps1 -WorkspaceRoot "D:\path\to\your\circuit\folder"
```

Then fully restart the IDE. Setup details are in [AGENTS.md](AGENTS.md). Day-to-day use is in the [user guide](docs/user-guide.md).

## Documentation

| Doc | Purpose |
| --- | --- |
| [User guide](docs/user-guide.md) | Install, run, and the limits of the GUI |
| [Tool reference](docs/tool_reference.md) | Every tool, with its required arguments |
| [Architecture](docs/architecture.md) | How a schematic becomes a simulation |
| [Error codes](docs/errors.md) | Stable codes on tool failures |
| [Security](docs/security.md) | What the sandbox does |
| [Changelog](CHANGELOG.md) | What shipped |

## License

MIT
