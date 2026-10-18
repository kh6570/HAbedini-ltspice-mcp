In the name of God, the Most Gracious, the Most Merciful

# Agent guide — LTspice MCP setup (Windows)

Use this when installing the LTspice MCP server in Cursor or VS Code.

The setup script adds an `ltspice` server. It does not remove a `qspice` server that is already configured.

| Client | User config |
| --- | --- |
| Cursor | `%USERPROFILE%\.cursor\mcp.json` |
| VS Code | `%APPDATA%\Code\User\mcp.json` |

## Setup

From this repository. `pip install` clones `mcp-app-core`. A checkout of it next to this repository is used instead when one is already there.

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\setup_mcp.ps1 -WorkspaceRoot "D:\path\to\your\circuit\folder"
```

Omit `-WorkspaceRoot` to use `%USERPROFILE%\Desktop\ltspice-mcp-test`.
Omit `-LtspiceExe` to probe `XVIIx64.exe` and `LTspice.exe`.

Then fully restart the IDE and confirm `ltspice` is connected.

Smoke prompt:

```text
Call describe_server_capabilities on the ltspice MCP server and summarize tool groups.
```

## Manual config

User-level configs need absolute paths.

- `PYTHON_EXE` — this repo's `.venv\Scripts\python.exe`
- `SIM_WORKSPACE` — folder of `.asc` files
- `LTSPICE_EXE` — for example `C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe`

Cursor root key is `mcpServers`. VS Code root key is `servers`.

```json
{
  "mcpServers": {
    "ltspice": {
      "type": "stdio",
      "command": "PYTHON_EXE",
      "args": ["-u", "-m", "ltspice_mcp", "--workspace-root", "SIM_WORKSPACE", "--log-level", "error"],
      "env": {
        "LTSPICE_EXE": "LTSPICE_EXE",
        "LTSPICE_LOG_LEVEL": "error"
      }
    }
  }
}
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Server missing | Re-run setup. The config must be in the user profile, with an absolute `command`. |
| Tools work, simulation fails | Check `LTSPICE_EXE` and that `--workspace-root` is a writable folder. |
| A run never returns | Do not pass `-b` on an `.asc` yourself. The server netlists first. Do not pass `-ini`; XVII 17.0.37 hangs on it. |
