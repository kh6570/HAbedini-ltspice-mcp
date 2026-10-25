In the name of God, the Most Gracious, the Most Merciful

# Agent guide — LTspice MCP setup (Windows)

Use this guide for the installation of the LTspice MCP server in Cursor or VS Code.

The setup script adds an `ltspice-mcp` server. The script does not remove a `qspice` server from the config.

| Client | User config |
| --- | --- |
| Cursor | `%USERPROFILE%\.cursor\mcp.json` |
| VS Code | `%APPDATA%\Code\User\mcp.json` |

## Setup

Run the setup command from this repository. `pip install` clones `mcp-app-core`. When a checkout of `mcp-app-core` is next to this repository, the setup uses that checkout instead.

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\setup_mcp.ps1 -WorkspaceRoot "D:\path\to\your\circuit\folder"
```

Omit `-WorkspaceRoot` to use `%USERPROFILE%\Desktop\ltspice-mcp-test`.
Omit `-LtspiceExe` to probe `XVIIx64.exe` and `LTspice.exe`.

Then fully restart the IDE. Confirm that `ltspice-mcp` has a connection.

Test prompt:

```text
Call describe_server_capabilities on the ltspice-mcp server.
Summarize the tool groups.
```

## Manual config

User-level configs need absolute paths.

- `PYTHON_EXE` — the `.venv\Scripts\python.exe` path in this repository
- `SIM_WORKSPACE` — the folder of `.asc` files
- `LTSPICE_EXE` — for example `C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe`

The Cursor root key is `mcpServers`. The VS Code root key is `servers`.

```json
{
  "mcpServers": {
    "ltspice-mcp": {
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

## Problems and fixes

| Symptom | Fix |
| --- | --- |
| The server is absent | Re-run setup. Put the config in the user profile. Use an absolute path for `command`. |
| The tools work. The simulation fails | Check `LTSPICE_EXE` and that `--workspace-root` is a writable folder. |
| A run never returns | Do not pass `-b` on an `.asc` yourself. The server netlists first. Do not pass `-ini`. XVII 17.0.37 hangs on `-ini`. |
