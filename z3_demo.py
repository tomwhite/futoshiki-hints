from z3 import *

# x = Int('x')
# y = Int('y')
# s = Solver()
# s.add(x > 10, y == x + 2)
# #s.add(y < 11)
# res = s.check()
# print(res)

# https://ericpony.github.io/z3py-tutorial/guide-examples.htm

X = [Int(f"x_{i}") for i in range(4)]
cells_c = [And(1 <= X[i], X[i] <= 4) for i in range(4)]
rows_c   = [Distinct([X[i] for i in range(4)])]

instance_c = [X[0] == 1, X[1] == 2, X[2] == 4]

# find solution
s = Solver()
s.add(cells_c + rows_c + instance_c)

res = s.check()
if res == sat:
    m = s.model()
    for i in range(4):
        print(m.evaluate(X[i]))
else:
    print("unsat")

# find if there is 0, 1, or more solutions to X[3]

s = Solver()
s.add(cells_c + rows_c + instance_c)

res = s.check()
if res == sat:
    m = s.model()
    for i in range(4):
        print(m.evaluate(X[i]))
    s.add(X[3] != s.model()[X[3]])
    if s.check() == sat:
        print(">1 solutions")
    else:
        print("no more solutions")
else:
    print("unsat")

# inequality

X = [Int(f"x_{i}") for i in range(2)]
cells_c = [And(1 <= X[i], X[i] <= 4) for i in range(2)]
ineq_c = [X[0] < X[1]]

instance_c = [X[1] == 2]

s = Solver()
s.add(cells_c + ineq_c + instance_c)

res = s.check()
if res == sat:
    m = s.model()
    for i in range(2):
        print(m.evaluate(X[i]))
    s.add(X[0] != s.model()[X[0]])
    if s.check() == sat:
        print(">1 solutions")
    else:
        print("no more solutions")
else:
    print("unsat")
