In the name of God, the Most Gracious, the Most Merciful

# LTspice directive cheatsheet

Summarized for this server from the LTspice XVII help and the Apache-2.0
[LTspice reference](https://github.com/analogdevicesinc/ltspice-reference).
This is not a copy of the LTspice manual.

Directives are `TEXT` lines in an `.asc` file whose content starts with `!`.

## Analysis

Only one of these should be active. This server comments the others out when a prepare tool replaces the analysis.

- `.tran <stop>` or `.tran <step> <stop> [start] [maxstep]`
- `.ac dec|oct|lin <points> <fstart> <fend>`
- `.dc <source> <start> <stop> <step>`
- `.op`
- `.noise <output> <source> dec|oct|lin <points> <fstart> <fend>`
- `.tf <output> <source>`

`.ac` only stimulates sources whose value includes `AC 1` (or another amplitude).

## Measurements and output

- `.meas TRAN name AVG V(out)` and the other `.meas` forms. Results are printed in the `.log`.
- `.four <frequency> V(out)`
- `.save V(out) I(R1)` limits what is written to the `.raw` file.
- `.options <name>=<value>`, for example `plotwinsize=0` to keep every transient point.

## Parameters and sweeps

- `.param name=value`
- `.func name(x) {expression}`
- `.step param name start stop step`
- `.step temp start stop step`
- `.ic V(out)=0`
- `.nodeset V(out)=1`

Monte Carlo in this server uses `mc(nominal, tolerance)` with `.step param run 1 N 1`.
`mc(x,y)` is a flat random value between `x*(1-y)` and `x*(1+y)`.

Two-corner worst case uses `table(corner, 1, low, 2, high)`.

## Libraries

- `.lib filename.lib`
- `.include filename.inc`
- `.model name type(parameters)`

`M` means milli. Mega is `Meg`. Write `u` for micro, not the micro sign.

## Network

- `.net <output> <source>` with optional `Rin=` and `Rout=`.
