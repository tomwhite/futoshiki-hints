import numpy as np
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


def test_refutation_scores():
    rep = """
·   ·   ·   ·
             
·   ·   ·   ·
^            
2   ·   ·   ·
    ^        
·   ·   ·   4
"""
    grid = Grid(rep)
    scores = refutation_scores(grid)

    # find minimum
    masked_scores = np.ma.masked_equal(scores, 0, copy=False)
    r, c = np.unravel_index(masked_scores.argmin(), scores.shape)

    assert r, c == (1, 0)


def test_refutation_value():
    rep = """
4   ·   ·   ·
             
1   ·   ·   ·
^            
2   ·   ·   ·
    ^        
3   ·   ·   4
"""
    grid = Grid(rep)
    scores = refutation_scores(grid)

    # find minimum
    masked_scores = np.ma.masked_equal(scores, 0, copy=False)
    r, c = np.unravel_index(masked_scores.argmin(), scores.shape)

    print(r, c)

def test_refutation_scores_5():
    rep = """
· < ·   ·   · > ·
    ^       v    
·   · < ·   ·   ·
    ^        
· < ·   ·   ·   ·
^               v
·   · < ·   ·   ·
^       ^        
· < ·   · > · > ·
"""
    grid = Grid(rep)
    print(grid)
    scores = refutation_scores(grid)
    print(scores)