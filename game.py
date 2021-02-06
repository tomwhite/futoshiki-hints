from futoshiki import *

# Guardian 2020-02-06
rep = """
·   · < ·   ·   ·
v   ^            
· > ·   ·   ·   ·
        ^       ^
·   · > · < · > ·
        ^        
·   · > ·   ·   ·
^                
·   ·   ·   · < ·
"""

if __name__ == "__main__":
    grid = Grid(rep)
    print("Start:")
    print(grid)
    print()

    i = 1
    while True:
        print("Press enter for hint...")
        input()
        print("Finding hint...")
        r, c, name, suggestion = hint(grid)
        v = solve(grid)[r, c]
        grid.values[r, c] = v
        print(suggestion)
        print(f"Move {i}:")
        print(grid)
        print()
        i += 1
