from blessed import Terminal
from futoshiki import *


class Game:
    """Play an interactive game of Futoshiki"""
    def __init__(self, term, grid):
        self.term = term
        self.grid = grid
        self.n = grid.n
        self.n_values = tuple(str(i) for i in range(1, self.n + 1))
        self.x = 0
        self.y = 0

    def print_grid(self):
        print(self.term.move_xy(0, 0) + str(self.grid))

    def print_message(self, message):
        print(self.term.move_xy(0, self.n * 2 - 1) + f"{message:<{80}}")

    def clear_message(self):
        print(self.term.move_xy(0, self.n * 2 - 1) + (" " * 80))

    def move_cursor(self, dx, dy):
        self.clear_char()
        self.x += dx
        self.y += dy
        self.reverse_char()

    def get_char_at(self):
        l = 4 * (self.n - 1) + 2
        return str(self.grid)[self.y * l + self.x]

    def clear_char(self):
        print(self.term.move_xy(self.x, self.y) + self.get_char_at())

    def reverse_char(self):
        print(self.term.move_xy(self.x, self.y) + self.term.reverse(self.get_char_at()))

    def set_value(self, value):
        if self.x % 4 == 0 and self.y % 2 == 0:
            r, c = self.y // 2, self.x // 4
            self.grid = self.grid.set(r, c, value)
            self.print_grid()
            self.reverse_char()

    def set_across(self, value):
        if self.x % 4 == 2 and self.y % 2 == 0:
            r, c = self.y // 2, (self.x - 1) // 4
            self.grid = self.grid.set_across(r, c, value)
            self.print_grid()
            self.reverse_char()

    def set_down(self, value):
        if self.x % 4 == 0 and self.y % 2 == 1:
            r, c = (self.y - 1) // 2, self.x // 4
            self.grid = self.grid.set_down(r, c, value)
            self.print_grid()
            self.reverse_char()

    def play(self):
        with self.term.fullscreen(), self.term.hidden_cursor():
            self.print_grid()
            self.reverse_char()
            with self.term.cbreak():
                val = ""
                while val.lower() != "q":
                    val = self.term.inkey()
                    if val.code == self.term.KEY_LEFT and self.x > 0:
                        self.move_cursor(-2, 0)
                    elif val.code == self.term.KEY_RIGHT and self.x < 4 * (self.n - 1):
                        self.move_cursor(2, 0)
                    elif val.code == self.term.KEY_UP and self.y > 0:
                        self.move_cursor(0, -1)
                    elif val.code == self.term.KEY_DOWN and self.y < 2 * (self.n - 1):
                        self.move_cursor(0, 1)
                    elif val in self.n_values:
                        self.set_value(int(val))
                        self.clear_message()
                    elif val == "<":
                        self.set_across(-1)
                        self.clear_message()
                    elif val == ">":
                        self.set_across(1)
                        self.clear_message()
                    elif val == "^":
                        self.set_down(-1)
                        self.clear_message()
                    elif val == "v":
                        self.set_down(1)
                        self.clear_message()
                    elif val in ("0", " ", "."):
                        # try them all
                        self.set_value(0)
                        self.set_across(0)
                        self.set_down(0)
                        self.clear_message()
                    elif val in ("h", "H"):
                        self.clear_char()
                        self.print_message("Finding hint...")
                        solution = solve(self.grid)
                        if solution is None:
                            self.print_message("No solution")
                            self.move_cursor(0, 0)
                            continue
                        r, c, name, suggestion = hint(self.grid)
                        self.move_cursor(0, 0)
                        self.print_message(suggestion)
                        if val == "H":
                            self.x = c * 4
                            self.y = r * 2
                            v = solution.values[r, c]
                            self.set_value(v)


if __name__ == "__main__":
    term = Terminal()
    grid = Grid.empty(5)
    game = Game(term, grid)
    game.play()
