import numpy as np


class Grid:
    """A Futoshiki grid."""

    def __init__(self, rep):
        self.rep = rep
        self.values, self.across, self.down = self.parse()

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
        lines = [line.ljust(width, "1") for line in lines]
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
                        rep += " "
                rep += "\n"
        return rep

    def __str__(self):
        return self.format()
