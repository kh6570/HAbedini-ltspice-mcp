In the name of God, the Most Gracious, the Most Merciful

# Debug convergence

1. Read the `.log`. A timestep-too-small or singular-matrix line is a convergence failure.
2. Add a path to ground for every node. An absent `FLAG ... 0` is the usual first problem.
3. Relax the analysis with `.options reltol=0.01` or a smaller maximum timestep.
4. For a switched circuit, start with `.op` or a shorter `.tran` before a long run.
5. Do not treat a warning as a failed run when `Total elapsed time` comes after the warning.
