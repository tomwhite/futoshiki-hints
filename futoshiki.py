import numpy as np
from z3 import And, Distinct, Int, Solver, sat, set_param, unsat

set_param(proof=True)


class Grid:
    """A Futoshiki grid."""

    def __init__(self, rep=None, values=None, across=None, down=None):
        if rep is not None:
            self.rep = rep
            self.values, self.across, self.down = self._parse()
        else:
            self.values = values
            self.across = across
            self.down = down
        self.n = self.values.shape[0]

    def _parse(self):
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

    def _format(self):
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
        return self._format()

    def set(self, r, c, val):
        """Set a cell to a value and return the new grid."""
        values = self.values.copy()
        values[r, c] = val
        return Grid(values=values, across=self.across, down=self.down)


def is_consistent(grid):
    n = grid.n

    # a variable for each cell (those undefined will not be used below)
    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(n)] for i in range(n)]

    # each (defined) cell contains a value in {1, ..., n}
    cells_c = [
        And(1 <= X[i][j], X[i][j] <= n)
        for i in range(n)
        for j in range(n)
        if grid.values[i, j] != 0
    ]

    # each row contains distinct values (for defined cells)
    rows_c = []
    for i in range(n):
        v = []
        for j in range(n):
            if grid.values[i, j] != 0:
                v.append(X[i][j])
        if len(v) > 0:
            rows_c.append(Distinct(v))

    # each column contains distinct values (for defined cells)
    cols_c = []
    for j in range(n):
        v = []
        for i in range(n):
            if grid.values[i, j] != 0:
                v.append(X[i][j])
        if len(v) > 0:
            cols_c.append(Distinct(v))

    # a variable for undefined cells that are only used for inequalities
    # this is for checking consistency of "1 > *" for example
    U = [[Int("u_%s_%s" % (i + 1, j + 1)) for j in range(n)] for i in range(n)]
    undefined_c = []

    def get(i, j):
        if grid.values[i][j] != 0:
            return X[i][j]
        undefined_c.append(And(1 <= U[i][j], U[i][j] <= n))
        return U[i][j]

    # add constraints for inequalities
    ineq_c = []
    for i, row in enumerate(grid.values):
        for j, _ in enumerate(row):
            if j < n - 1:
                ineq = grid.across[i, j]
                if ineq == -1:
                    ineq_c.append(get(i, j) < get(i, j + 1))
                elif ineq == 1:
                    ineq_c.append(get(i, j) > get(i, j + 1))
        if i < n - 1:
            for j, _ in enumerate(row):
                ineq = grid.down[i, j]
                if ineq == -1:
                    ineq_c.append(get(i, j) < get(i + 1, j))
                elif ineq == 1:
                    ineq_c.append(get(i, j) > get(i + 1, j))

    # each cell has the value provided
    instance_c = [
        X[i][j] == int(grid.values[i, j])
        for i in range(n)
        for j in range(n)
        if grid.values[i, j] != 0
    ]

    # solve
    s = Solver()
    s.add(cells_c + rows_c + cols_c + ineq_c + instance_c + undefined_c)
    return s.check() == sat


def _get_variables_and_constraints(grid):
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

    return X, cells_c + rows_c + cols_c + ineq_c + instance_c


def solve(grid):
    s = Solver()
    X, constraints = _get_variables_and_constraints(grid)
    s.add(constraints)
    if s.check() == sat:
        m = s.model()
        n = grid.n
        values = np.empty((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                values[i, j] = m.evaluate(X[i][j]).as_long()
        return Grid(values=values, across=grid.across, down=grid.down)
    else:
        return None


def refutation_scores(grid):
    X, constraints = _get_variables_and_constraints(grid)
    s = Solver()
    s.set(unsat_core=True)
    s.add(constraints)

    n = grid.n
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


class RowAndColumnExclusionRule:
    """For a given cell there is only one value that can go into the cell."""

    def __init__(self):
        self.name = "exclusion"

    def apply(self, grid, r=None, c=None):
        if r is None:
            r_range = range(grid.n)
        else:
            r_range = range(r, r + 1)
        if c is None:
            c_range = range(grid.n)
        else:
            c_range = range(c, c + 1)
        for r in r_range:
            for c in c_range:
                if grid.values[r, c] != 0:
                    continue
                vals = self.possible_values(grid, r, c)
                if len(vals) == 1:
                    val = next(iter(vals))
                    suggestion = (
                        f"What is the only value that can go in ({r + 1}, {c + 1})?"
                    )
                    return r, c, val, suggestion
        return None

    def possible_values(self, grid, r, c):
        vals = set(range(1, grid.n + 1))
        for val in range(1, grid.n + 1):
            if not is_consistent(grid.set(r, c, val)):
                vals.discard(val)
        return vals


class RowInclusionRule:
    """For a given row there exists only one cell which can contain a given value."""

    def __init__(self):
        self.name = "row inclusion"

    def possible_cells(self, grid, val, r):
        cells = []
        for c in range(grid.n):
            if grid.values[r, c] != 0:
                continue
            if is_consistent(grid.set(r, c, val)):
                cells.append((r, c))
        return cells

    def apply(self, grid, r=None):
        if r is None:
            r_range = range(grid.n)
        else:
            r_range = range(r, r + 1)
        for r in r_range:
            for val in range(1, grid.n + 1):
                cells = self.possible_cells(grid, val, r=r)
                if len(cells) == 1:
                    r, c = cells[0]
                    # Less of a hint: Which cell in row r does one number have to go?
                    suggestion = (
                        f"Where in row {r + 1} does the number {val} have to go?"
                    )
                    return r, c, val, suggestion
        return None


class ColumnInclusionRule:
    """For a given column there exists only one cell which can contain a given value."""

    def __init__(self):
        self.name = "column inclusion"

    def possible_cells(self, grid, val, c):
        cells = []
        for r in range(grid.n):
            if grid.values[r, c] != 0:
                continue
            if is_consistent(grid.set(r, c, val)):
                cells.append((r, c))
        return cells

    def apply(self, grid, c=None):
        if c is None:
            c_range = range(grid.n)
        else:
            c_range = range(c, c + 1)
        for c in c_range:
            for val in range(1, grid.n + 1):
                cells = self.possible_cells(grid, val, c=c)
                if len(cells) == 1:
                    r, c = cells[0]
                    # Less of a hint: Which cell in column c does one number have to go?
                    suggestion = (
                        f"Where in column {c + 1} does the number {val} have to go?"
                    )
                    return r, c, val, suggestion
        return None


class MinimumRefutationScoreRule:
    """Find a cell that requires the fewest number of simple steps to demonstrate
    the inconsistency of each wrong candidate value."""

    def __init__(self):
        self.name = "refutation"

    def apply(self, grid):
        scores = refutation_scores(grid)
        masked_scores = np.ma.masked_equal(scores, 0, copy=False)
        r, c = np.unravel_index(masked_scores.argmin(), scores.shape)
        suggestion = f"Can you show that all numbers except one for ({r + 1}, {c + 1}) are impossible?"
        return r, c, None, suggestion  # TODO: fill in value


def hint(grid):
    rules = (
        RowAndColumnExclusionRule(),
        RowInclusionRule(),
        ColumnInclusionRule(),
        MinimumRefutationScoreRule(),
    )
    for rule in rules:
        res = rule.apply(grid)
        if res is not None:
            r, c, val, suggestion = res
            return r, c, rule.name, suggestion


def play(grid, n_moves=5):
    print("Start:")
    print(grid)
    print()
    for i in range(1, n_moves + 1):
        r, c, name, suggestion = hint(grid)
        val = solve(grid).values[r, c]
        grid.values[r, c] = val
        print(suggestion)
        print(f"Move {i}:")
        print(grid)
        print()
