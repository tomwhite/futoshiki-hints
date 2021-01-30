import numpy as np
from z3 import *

grid = np.array(
    [
        [3, 0, 1, 2],
        [0, 0, 2, 0],
        [0, 0, 0, 3],
        [1, 0, 0, 4],
    ]
)


def apply_row_exclusion_rule(grid, r, c):
    n = grid.shape[0]
    X = [Int(f"x_{i}") for i in range(n)]
    cells_c = [And(1 <= X[i], X[i] <= n) for i in range(n)]
    rows_c = [Distinct([X[i] for i in range(n)])]
    instance_c = [
        If(int(grid[r, j]) == 0, True, X[j] == int(grid[r, j])) for j in range(n)
    ]

    # find solution
    s = Solver()
    s.add(cells_c + rows_c + instance_c)

    if s.check() == sat:
        m = s.model()
        val = m.evaluate(X[c])
        s.add(X[c] != s.model()[X[c]])
        if s.check() == sat:
            return 2, None
        else:
            return 1, val
    return 0, None


def apply_col_exclusion_rule(grid, r, c):
    n = grid.shape[0]
    X = [Int(f"x_{i}") for i in range(n)]
    cells_c = [And(1 <= X[i], X[i] <= n) for i in range(n)]
    rows_c = [Distinct([X[i] for i in range(n)])]
    instance_c = [
        If(int(grid[i, c]) == 0, True, X[i] == int(grid[i, c])) for i in range(n)
    ]

    # find solution
    s = Solver()
    s.add(cells_c + rows_c + instance_c)

    if s.check() == sat:
        m = s.model()
        val = m.evaluate(X[r])
        s.add(X[r] != s.model()[X[r]])
        if s.check() == sat:
            return 2, None
        else:
            return 1, val
    return 0, None


n_solutions, val = apply_row_exclusion_rule(grid, 0, 1)
print(n_solutions, val)

n_solutions, val = apply_col_exclusion_rule(grid, 1, 3)
print(n_solutions, val)
