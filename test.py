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


def test_rule():
    rep = """
3   ·   1   2
             
·   ·   2   ·
             
·   ·   ·   3
             
1   ·   ·   4
"""
    grid = Grid(rep)
    rule = RowAndColumnExclusionRule()
    assert rule.apply(grid, 1, 1) is None
    assert rule.apply(grid, 0, 1) == 4
    assert rule.apply(grid, 2, 2) == 4
    assert rule.apply(grid, 1, 3) == 1


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
    # from https://krazydad.com/tablet/futoshiki/?kind=4x4&volumeNumber=1&bookNumber=1&puzzleNumber=3

    rep = """
·   ·   ·   ·
             
·   ·   ·   ·
^            
2   ·   ·   ·
    ^        
·   ·   ·   4
"""
    grid = Grid(rep)
    r, c = hint(grid)
    assert r == 1
    assert c == 0

    rep = """
·   ·   ·   ·
             
1   ·   ·   ·
^            
2   ·   ·   ·
    ^        
·   ·   ·   4
"""
    grid = Grid(rep)
    r, c = hint(grid)
    print(refutation_scores(grid))
    assert r == 3
    assert c == 0

    rep = """
·   ·   ·   ·
             
1   ·   ·   ·
^            
2   ·   ·   ·
    ^        
3   ·   ·   4
"""
    grid = Grid(rep)
    r, c = hint(grid)
    assert r == 0
    assert c == 0

    rep = """
4   ·   ·   ·
             
1   ·   ·   ·
^            
2   ·   ·   ·
    ^        
3   ·   ·   4
"""
    grid = Grid(rep)
    r, c = hint(grid)
    assert r == 3
    assert c == 1


def test_refutation_scores_guardian_2021_01_16():
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
    scores = refutation_scores(grid)
    # I think 0,0 is easiest, not 1,1 - but still helpful
    print(scores)

def test_play():
    rep = """
·   1   ·   ·
^           ^
·   ·   ·   ·
v            
·   ·   ·   ·
            ^
·   ·   ·   ·
"""
    grid = Grid(rep)
    print(solve(grid))
    print(refutation_scores(grid))
    # play(grid)