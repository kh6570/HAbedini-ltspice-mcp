In the name of God, the Most Gracious, the Most Merciful

# Errors

Tool failures use `LTspiceError`. The MCP error payload includes `error_code` and `error_type`.

| Code | Meaning |
| --- | --- |
| `ltspice_error` | Fallback |
| `backend_unavailable` | LTspice was not found |
| `artifact_missing` | A log, raw, or netlist was not produced |
| `content_conflict` | A schematic save was refused because the file changed since the last read |
| `schematic_invalid` | The `.asc` structure cannot support the edit |
| `batch_conflict` | A batch manifest is unusable |
| `timeout_exceeded` | The run exceeded `LTSPICE_TIMEOUT_S` |
| `simulation_failed` | LTspice stopped without `Total elapsed time` |
| `convergence_failed` | Timestep, singular matrix, or a failed analysis |
| `parse_failed` | A schematic, raw file, or log could not be read |
| `budget_exceeded` | A waveform could not be reduced to the budget |
| `sandbox_violation` | A path escaped the workspace |
| `validation_failed` | The arguments were inconsistent |
| `configuration_invalid` | Settings are missing or invalid |
| `unsupported` | LTspice has no equivalent, including GUI commands |
| `unsupported_manifest_version` | A saved manifest is too new |
