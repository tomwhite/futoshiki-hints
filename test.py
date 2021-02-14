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


def test_is_consistent():
    assert (
        is_consistent(
            Grid(
                """
1   ·
     
·   ·
"""
            )
        )
        == True
    )

    assert (
        is_consistent(
            Grid(
                """
·   ·
     
3   ·
"""
            )
        )
        == False
    )

    assert (
        is_consistent(
            Grid(
                """
1   1
     
·   ·
"""
            )
        )
        == False
    )

    assert (
        is_consistent(
            Grid(
                """
1   ·
     
1   ·
"""
            )
        )
        == False
    )

    assert (
        is_consistent(
            Grid(
                """
1 > 2
     
·   ·
"""
            )
        )
        == False
    )

    assert (
        is_consistent(
            Grid(
                """
1   ·
v    
2   ·
"""
            )
        )
        == False
    )

    # note this is consistent, even though it doesn't give a solution
    assert (
        is_consistent(
            Grid(
                """
3   ·   1
         
·   1   2
         
·   ·   ·
"""
            )
        )
        == True
    )

    assert (
        is_consistent(
            Grid(
                """
1 > ·
     
·   ·
"""
            )
        )
        == False
    )


def test_exclusion_rule():
    rep = """
3   ·   1   2
             
·   ·   2   ·
             
·   ·   ·   3
             
1   ·   ·   4
"""
    grid = Grid(rep)
    rule = RowAndColumnExclusionRule()
    assert rule.apply(grid, 1, 1) is None
    assert rule.apply(grid, 0, 1) == (
        0,
        1,
        4,
        "What is the only value that can go in (1, 2)?",
    )
    assert rule.apply(grid, 2, 2) == (
        2,
        2,
        4,
        "What is the only value that can go in (3, 3)?",
    )
    assert rule.apply(grid, 1, 3) == (
        1,
        3,
        1,
        "What is the only value that can go in (2, 4)?",
    )

    rep = """
·   ·   ·   ·
             
·   ·   ·   ·
^            
2   ·   ·   ·
    ^        
·   ·   ·   4
"""
    grid = Grid(rep)
    rule = RowAndColumnExclusionRule()
    suggestion = "What is the only value that can go in (2, 1)?"
    assert rule.apply(grid, 1, 0) == (1, 0, 1, suggestion)


def test_inclusion_rule():
    # based on https://www.futoshiki.org/how-to-solve
    rep = """
3   ·   · > ·
    v        
·   ·   ·   ·
             
·   ·   ·   ·
        ^    
· > ·   ·   ·
"""
    grid = Grid(rep)
    rule = RowInclusionRule()
    suggestion = "Where in row 1 does the number 1 have to go?"
    assert rule.apply(grid, r=0) == (0, 3, 1, suggestion)

    rep = """
3   ·   ·   ·
            v
· > ·   ·   ·
             
·   ·   · < ·
v            
·   ·   ·   ·
"""
    grid = Grid(rep)
    rule = ColumnInclusionRule()
    suggestion = "Where in column 1 does the number 1 have to go?"
    assert rule.apply(grid, c=0) == (3, 0, 1, suggestion)


def test_refutation_score_guardian_2021_01_16():
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
    rule = MinimumRefutationScoreRule()
    suggestion = "Can you show that all numbers except one for (2, 2) are impossible?"
    assert rule.apply(grid) == (1, 1, None, suggestion)


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
        solution.values,
        np.array(
            [
                [4, 3, 2, 1],
                [1, 4, 3, 2],
                [2, 1, 4, 3],
                [3, 2, 1, 4],
            ]
        ),
    )


def test_hint():
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
    r, c, name, suggestion = hint(grid)
    assert r == 1
    assert c == 0
    assert name == "exclusion"

    rep = """
·   ·   ·   ·
             
1   ·   ·   ·
^            
2   ·   ·   ·
    ^        
·   ·   ·   4
"""
    grid = Grid(rep)
    r, c, name, suggestion = hint(grid)
    assert r == 3
    assert c == 0
    assert name == "exclusion"

    rep = """
·   ·   ·   ·
             
1   ·   ·   ·
^            
2   ·   ·   ·
    ^        
3   ·   ·   4
"""
    grid = Grid(rep)
    r, c, name, suggestion = hint(grid)
    assert r == 0
    assert c == 0
    assert name == "exclusion"

    rep = """
4   ·   ·   ·
             
1   ·   ·   ·
^            
2   ·   ·   ·
    ^        
3   ·   ·   4
"""
    grid = Grid(rep)
    r, c, name, suggestion = hint(grid)
    assert r == 3
    assert c == 1
    assert name == "exclusion"


def test_hint_inclusion():
    # from https://www.futoshiki.org/how-to-solve
    rep = """
3   ·   · > ·
    v        
·   ·   3   ·
             
·   ·   ·   ·
        ^    
· > ·   ·   ·
"""
    grid = Grid(rep)
    r, c, name, suggestion = hint(grid)
    assert r == 0
    assert c == 3
    assert name == "row inclusion"


def test_hint_inclusion_guardian_2021_01_16():
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
    r, c, name, suggestion = hint(grid)
    assert r == 3
    assert c == 3
    assert name == "row inclusion"


def test_hint_inclusion_iterating_possibilities():
    # from https://www.futoshiki.org/how-to-solve
    rep = """
·   ·   4   ·
v            
·   4 > ·   ·
             
·   · < · < 4
             
4   ·   · < 3
"""
    grid = Grid(rep)
    r, c, name, suggestion = hint(grid)
    assert r == 0
    assert c == 1
    assert name == "column inclusion"


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
    play(grid, n_moves=6)


# def test_difficult_13():
#     # https://krazydad.com/futoshiki/sfiles/FUT_5x_v1_b100.pdf #13
#     rep = """
# · > ·   · < ·   ·
#     v       ^
# · < ·   ·   ·   ·

# ·   ·   ·   ·   ·

# ·   ·   3   ·   ·
#                 ^
# ·   · > ·   · > ·
# """
#     grid = Grid(rep)
#     play(grid, n_moves=3)
#     # TODO: assert it does a refutation score


# def test_difficult_16():
#     # https://krazydad.com/futoshiki/sfiles/FUT_5x_v1_b100.pdf #16
#     rep = """
# ·   ·   ·   ·   ·
# ^
# · < ·   ·   · > ·
# ^               v
# ·   · > ·   ·   ·
# v           v
# ·   ·   ·   · > ·

# ·   ·   ·   ·   ·
# """
#     grid = Grid(rep)
#     play(grid, n_moves=3)
#     # TODO: assert it does a refutation score
