In the name of God, the Most Gracious, the Most Merciful

# Errors

Tool failures use `LTspiceError`. The MCP error payload includes `error_code` and `error_type`.

| Code | Definition |
| --- | --- |
| `ltspice_error` | Fallback |
| `backend_unavailable` | The server did not find LTspice |
| `artifact_missing` | The run did not produce a log, a raw file, or a netlist |
| `content_conflict` | The server refused a schematic save because the file changed since the last read |
| `schematic_invalid` | The `.asc` structure cannot support the edit |
| `batch_conflict` | A batch manifest is unusable |
| `timeout_exceeded` | The run exceeded `LTSPICE_TIMEOUT_S` |
| `simulation_failed` | LTspice stopped without `Total elapsed time` |
| `convergence_failed` | Timestep, singular matrix, or a failed analysis |
| `parse_failed` | The server could not read a schematic, a raw file, or a log |
| `budget_exceeded` | The server could not reduce a waveform to the budget |
| `sandbox_violation` | A path escaped the workspace |
| `validation_failed` | The arguments were inconsistent |
| `configuration_invalid` | The settings are absent or invalid |
| `unsupported` | LTspice has no equivalent, for example GUI commands |
| `unsupported_manifest_version` | A saved manifest is too new |
