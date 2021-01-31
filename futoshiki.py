import numpy as np
from z3 import And, Distinct, Int, Solver, sat, set_param, unsat

set_param(proof=True)


class Grid:
    """A Futoshiki grid."""

    def __init__(self, rep):
        self.rep = rep
        self.values, self.across, self.down = self.parse()
        self.n = self.values.shape[0]

    def parse(self):
        # encode characters as ints
        # note that inequalities have one subtracted later, hence space is 1 here
        table = str.maketrans("· <>^v", "010202")
        rep = self.rep.translate(table)
        # split into lines
        lines = rep.strip().splitlines()
        # make sure each line is the same length
        height = len(lines)
        width = 2 * height - 1
        lines = [line.ljust(width, "1")[:width] for line in lines]
        # turn into a numpy array
        a = np.array([list(line) for line in lines], dtype=int)
        # slice into values and across/down inequalities
        values = a[::2, ::4]
        across = a[::2, 2::4] - 1
        down = a[1::2, ::4] - 1
        return values, across, down

    def format(self):
        def format_value(x):
            return f"{x}" if x > 0 else "·"

        def format_across(x):
            if x == -1:
                return " < "
            elif x == 1:
                return " > "
            else:
                return "   "

        def format_down(x):
            if x == -1:
                return "^   "
            elif x == 1:
                return "v   "
            else:
                return "    "

        rep = ""
        for i, row in enumerate(self.values):
            for j, val in enumerate(row):
                rep += format_value(val)
                if j < len(self.values) - 1:
                    rep += format_across(self.across[i, j])
            rep += "\n"
            if i < len(self.values) - 1:
                for j, _ in enumerate(row):
                    if j < len(self.values) - 1:
                        rep += format_down(self.down[i, j])
                    else:
                        rep += format_down(self.down[i, j])[0]
                rep += "\n"
        return rep

    def __str__(self):
        return self.format()


class Rule:

    def possible_values(self, grid, r, c):
        pass

    def apply(self, grid, r, c):
        vals = self.possible_values(grid, r, c)
        if len(vals) == 1:
            val = next(iter(vals))
            return val
        return None


class RowAndColumnExclusionRule(Rule):

    def possible_values(self, grid, r, c):
        vals = set(range(1, grid.n + 1))
        for i, row in enumerate(grid.values):
            for j, val in enumerate(row):
                if (i == r) != (j == c): # xor
                    if val != 0:
                        vals.discard(val)
        return vals


class MinExclusionRule:

    def possible_values(self, grid, r, c):
        vals = set(range(1, grid.n + 1))
        # TODO: iterate over less than and find any where it's 2
        return vals


def solve(grid):
    n = grid.n

    # a variable for each cell
    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(n)] for i in range(n)]

    # each cell contains a value in {1, ..., n}
    cells_c = [And(1 <= X[i][j], X[i][j] <= n) for i in range(n) for j in range(n)]

    # each row contains distinct values
    rows_c = [Distinct(X[i]) for i in range(n)]

    # each column contains distinct values
    cols_c = [Distinct([X[i][j] for i in range(n)]) for j in range(n)]

    # add constraints for inequalities
    ineq_c = []
    for i, row in enumerate(grid.values):
        for j, _ in enumerate(row):
            if j < n - 1:
                ineq = grid.across[i, j]
                if ineq == -1:
                    ineq_c.append(X[i][j] < X[i][j + 1])
                elif ineq == 1:
                    ineq_c.append(X[i][j] > X[i][j + 1])
        if i < n - 1:
            for j, _ in enumerate(row):
                ineq = grid.down[i, j]
                if ineq == -1:
                    ineq_c.append(X[i][j] < X[i + 1][j])
                elif ineq == 1:
                    ineq_c.append(X[i][j] > X[i + 1][j])

    # add constraints for any values provided
    instance_c = [
        X[i][j] == int(grid.values[i, j])
        for i in range(n)
        for j in range(n)
        if grid.values[i, j] != 0
    ]

    # solve
    s = Solver()
    s.add(cells_c + rows_c + cols_c + ineq_c + instance_c)
    if s.check() == sat:
        m = s.model()
        values = np.empty((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                values[i, j] = m.evaluate(X[i][j]).as_long()
        # TODO: return grid
        return values
    else:
        return None


def refutation_scores(grid):
    n = grid.n

    # a variable for each cell
    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(n)] for i in range(n)]

    # each cell contains a value in {1, ..., n}
    cells_c = [And(1 <= X[i][j], X[i][j] <= n) for i in range(n) for j in range(n)]

    # each row contains distinct values
    rows_c = [Distinct(X[i]) for i in range(n)]

    # each column contains distinct values
    cols_c = [Distinct([X[i][j] for i in range(n)]) for j in range(n)]

    # add constraints for inequalities
    ineq_c = []
    for i, row in enumerate(grid.values):
        for j, _ in enumerate(row):
            if j < n - 1:
                ineq = grid.across[i, j]
                if ineq == -1:
                    ineq_c.append(X[i][j] < X[i][j + 1])
                elif ineq == 1:
                    ineq_c.append(X[i][j] > X[i][j + 1])
        if i < n - 1:
            for j, _ in enumerate(row):
                ineq = grid.down[i, j]
                if ineq == -1:
                    ineq_c.append(X[i][j] < X[i + 1][j])
                elif ineq == 1:
                    ineq_c.append(X[i][j] > X[i + 1][j])

    # add constraints for any values provided
    instance_c = [
        X[i][j] == int(grid.values[i, j])
        for i in range(n)
        for j in range(n)
        if grid.values[i, j] != 0
    ]

    # calculate scores
    s = Solver()
    s.set(unsat_core=True)
    s.add(cells_c + rows_c + cols_c + ineq_c + instance_c)

    scores = np.zeros((n, n), dtype=int)
    for r in range(0, n):
        for c in range(0, n):
            if grid.values[r, c] != 0:
                continue
            for v in range(1, n + 1):
                s.push()
                s.add(X[r][c] == v)
                if s.check() == unsat:
                    scores[r, c] += len(s.proof().sexpr().splitlines())
                s.pop()
    return scores

def hint(grid):
    scores = refutation_scores(grid)
    masked_scores = np.ma.masked_equal(scores, 0, copy=False)
    r, c = np.unravel_index(masked_scores.argmin(), scores.shape)
    return r, c

def play(grid, n_moves=5):
    print("Start:")
    print(grid)
    print()
    for i in range(1, n_moves + 1):
        r, c = hint(grid)
        v = solve(grid)[r, c]
        grid.values[r, c] = v
        print(f"Move {i}:")
        print(grid)
        print()
