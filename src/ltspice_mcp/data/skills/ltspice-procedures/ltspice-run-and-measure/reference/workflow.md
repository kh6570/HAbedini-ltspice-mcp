In the name of God, the Most Gracious, the Most Merciful

# Run and measure

1. Keep the `.asc` file as the source of truth.
2. Add one analysis directive, such as `.tran` or `.ac`.
3. Add a `.meas` directive for the number you need.
4. Call `run_simulation`.
5. Read the measurement from the `.log` with `read_measures`.
6. Use `read_waveform` when you need the trace. Stay inside the 2000 point budget.
