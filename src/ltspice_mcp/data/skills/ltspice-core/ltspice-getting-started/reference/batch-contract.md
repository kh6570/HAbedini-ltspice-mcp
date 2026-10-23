In the name of God, the Most Gracious, the Most Merciful

# Batch contract

An `.asc` is netlisted with `-netlist`, then the sibling `.net` is run with `-b -ascii`. Never pass `-b` to an `.asc`: that opens the LTspice window and does not return. Waveform reads stay inside the 2000 point budget; prefer `read_measures` when a scalar is enough.

Directives such as `.tran` are `!.tran` text on the schematic. Stage one with `prepare_transient` or another prepare tool, then call `run_simulation`.
