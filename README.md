# Futoshiki

It's easy to solve a Futoshiki puzzle using a computer, but it's not very
illuminating as the solution doesn't tell you the steps or reasoning to get to
it.

It would be nice to get a suggestion if you get stuck when doing a puzzle.

This project is an attempt to remedy this. Given a Futoshiki grid, the program
will give a hint for the next simplest step in solving the grid.

For example, given the following 4-by-4 grid

```
·   ·   ·   ·
             
·   ·   ·   ·
^            
2   ·   ·   ·
    ^        
·   ·   ·   4
```

the program will ask _"What is the only value that can go in (2, 1)?"_

The answer is 1, since it is the only value in the range 1-4 that is less than 2.

This grid is a bit harder:

```
3   ·   · > ·
    v        
·   ·   ·   ·
             
·   ·   ·   ·
        ^    
· > ·   ·   ·
```

The hint in this case is _"Where in row 1 does the number 1 have to go?"_

The number 1 has to go at the end of the row, since it can't be greater than another number.

## Refutation score

The process of generating suggestions rests on an idea from the paper
_Difficulty Rating of Sudoku Puzzles: An Overview and Evaluation_ by Radek Pelanek.

> Let us suppose that we have a state in which the specified simple techniques do not yield any progress. For each unassigned variable (empty cell) we compute a “refutation score”, this score expresses the difficulty of assigning the correct value to this variable in the given state by refuting all other possible candidates.

Using this idea we compute the refutation score for every unfilled square in the grid,
then suggest the square with the lowest score as the one for the user to look at.

To compute the refutation score I used the Z3 theorem prover. It has the ability to produce a
symbolic [proof](https://theory.stanford.edu/~nikolaj/programmingz3.html#sec-proofs) of "usatisfiability" - in other words, a proof of why a candidate value does not have a solution.

To illustrate this, consider this difficult puzzle ([Krazydad Volume 1, Book 100, #16](https://krazydad.com/futoshiki/index.php?sv=DL&pf=sfiles/FUT_5x_v1_b100.pdf&title=5x5%20Futoshiki%20Puzzles,%20Volume%201,%20Book%20100)):

```
·   ·   ·   ·   ·
^                
· < ·   1   · > ·
^               v
·   · > ·   ·   1
v           v    
·   ·   ·   · > ·
                 
·   ·   ·   ·   ·
```

It turns out that the centre square has the value 2. The Z3 solver will find a proof showing why the value
1 is not solvable (this one is simple: there's already a 1 in the same row), why 3 is not solvable,
why 4 is not solvable, and why 5 is not solvable.

The proofs in each case are not easily interpretable, however it _is_ possible to use their lengths as
proxies for their complexity. So the refutation score is simply the sum of the lengths of the proofs.

Doing this for each unfilled square, we get the following scores:

```
[[ 740 2573 3869 1087 2158]
 [ 510  984    0  542  882]
 [ 495  652  360  573    0]
 [ 975 2301 1160  274  297]
 [1836 4409 3059 1251 2366]]
```

Square (4, 4) has the lowest score, so is in some sense the easiest one to find the value for, by
showing all candidates (except one) produce a contradiction.

## Simple rules

The refutation score is only used if squares can't be filled using simple rules. It turns out
these can be applied in most cases, and are easier for the human mind to apply than the refutation
strategy - which is usually a fallback of last resort.

From the above paper there are two simple rules:

> __Naked single technique__ (also called singleton, single value, forced value, exclusion principle):
    For a given cell there is only one value that can go into the cell, because all other values occur in row, column or sub-grid of the cell (any other number would lead to a direct violation of rules).
> __Hidden single technique__ (also called naked value, inclusion principle):
    For a given unit (row, column or sub-grid) there exists only one cell which can contain a given value (all other placements would lead to a direct violation of rules).

These are for Sudoku, but they apply to Futoshiki too. In the implementation here there are four rules, applied in order:
1. `RowAndColumnExclusionRule` - exclusion applied to rows and columns
2. `RowInclusionRule` - inclusion applied to rows
3. `ColumnInclusionRule` - inclusion applied to columns
4. `MinimumRefutationScoreRule` - a fallback rule using minimum refutation score

(Conceptually `RowInclusionRule` and `ColumnInclusionRule` are instances of the same rule, they are just broken into two for ease of implementation.)

All the rules are implemented using Z3, since it makes specifying the constraints very straightforward.
