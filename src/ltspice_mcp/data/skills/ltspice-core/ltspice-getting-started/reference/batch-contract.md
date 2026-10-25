In the name of God, the Most Gracious, the Most Merciful

# Batch contract

LTspice netlists an `.asc` with `-netlist`. Then LTspice runs the sibling `.net` with `-b -ascii`. Never pass `-b` to an `.asc`: that opens the LTspice window and does not return. Waveform reads stay inside the 2000 point budget. Prefer `read_measures` when a scalar is enough.

Directives such as `.tran` are `!.tran` text on the schematic. Stage one with `prepare_transient` or another prepare tool. Then call `run_simulation`.
