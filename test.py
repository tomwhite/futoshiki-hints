from numpy.testing import assert_array_equal
from futoshiki import *

blank = """
·   ·   ·   ·
             
·   ·   ·   ·
             
·   ·   ·   ·
             
·   ·   ·   ·
"""


def test_grid():
    rep = """
· < ·   ·   ·
        v    
1   ·   ·   ·
        ^    
·   ·   ·   ·
v   ^        
·   ·   ·   ·
"""
    grid = Grid(rep)
    assert_array_equal(
        grid.values,
        np.array(
            [
                [0, 0, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]
        ),
    )
    assert_array_equal(
        grid.across, np.array([[-1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
    )
    assert_array_equal(
        grid.down,
        np.array(
            [
                [0, 0, 1, 0],
                [0, 0, -1, 0],
                [1, -1, 0, 0],
            ]
        ),
    )

    assert str(Grid(rep)).strip() == rep.strip()


def test_solve():
    rep = """
·   ·   ·   ·
             
·   ·   ·   ·
^            
2   ·   ·   ·
    ^        
·   ·   ·   4
"""
    grid = Grid(rep)
    solution = solve(grid)
    assert_array_equal(
        solution,
        np.array(
            [
                [4, 3, 2, 1],
                [1, 4, 3, 2],
                [2, 1, 4, 3],
                [3, 2, 1, 4],
            ]
        ),
    )


def test_refutation_value():
    rep = """
·   ·   ·   ·
             
·   ·   ·   ·
^            
2   ·   ·   ·
    ^        
·   ·   ·   4
"""
    grid = Grid(rep)
    rv = refutation_value(grid)
    print(rv)