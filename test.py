import LA
mm = LA.Make_Matrix()
mo = LA.Matrix_Operations()
vo = LA.Vector_Operations()

"""operators = ["+", "-", "/", "*", "^"]

def account_for_var(statement):
    for x in statement:
        if x in operators:
            print(x)

s = "(a - b) * (a + b)"
account_for_var(s)
"""

m = mm.make_random_matrix(3, 4)
mo.print_matrix(m)
mo.print_matrix(mo.RREF(m))
