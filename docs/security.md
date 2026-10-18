In the name of God, the Most Gracious, the Most Merciful

# Security

The server is a local process. It is not a remote simulation service.

- Every schematic, netlist, log, raw, and export path is resolved against the workspace root. A path outside that root raises `sandbox_violation`.
- Zip import rejects entries that would write outside the destination directory.
- Extra simulator switches cannot contain path characters, and `-b`, `-ascii`, `-netlist`, `-ini`, and `-run` cannot be passed through.
- Batch simulation runs the installed LTspice executable. It does not download models and it does not execute schematic text as Python.
- `write_workspace_text_file` only creates files inside the workspace.
- GUI launch starts `LTspice.exe` or `XVIIx64.exe` on a workspace schematic. It cannot send keystrokes or read the window.
- There is no C++ toolchain. The server does not invoke a compiler.

Set `--workspace-root` to the folder that holds the circuits you want the assistant to edit.
