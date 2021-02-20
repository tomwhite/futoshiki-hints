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

# Guardian 2020-02-13 Hard
rep = """
·   · > · > ·   ·
            ^    
·   ·   ·   · < ·
^                
·   · > ·   ·   ·
        v   ^    
·   ·   · < · > ·
    v   v   ^    
· > ·   ·   ·   ·
"""

# Guardian 2020-02-20 Easy
rep = """
· > ·   ·   ·   ·
^   v            
4   ·   · < ·   ·
v       ^        
2   4   ·   ·   ·
        ^       ^
·   ·   · > · < ·
            ^   v
·   ·   ·   · > ·
"""

if __name__ == "__main__":
    grid = Grid(rep)
    print("Start:")
    print(grid)
    print()

    i = 1
    while True:
        if grid.filled():
            break
        print("Press enter for hint...")
        input()
        print("Finding hint...")
        r, c, name, suggestion = hint(grid)
        v = solve(grid).values[r, c]
        grid.values[r, c] = v
        print(suggestion)
        print(f"Move {i}:")
        print(grid)
        print()
        i += 1
