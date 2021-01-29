import numpy as np


class Grid:
    """A Futoshiki grid."""

    def __init__(self, rep):
        self.rep = rep
        self.values, self.across, self.down = Grid.parse(rep)

    @staticmethod
    def parse(rep):
        # encode characters as ints
        # note that inequalities have one subtracted later, hence space is 1 here
        table = str.maketrans("· <>^v", "010202")
        rep = rep.translate(table)
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

    def __str__(self):
        return self.rep
