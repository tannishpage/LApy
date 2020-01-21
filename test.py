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

G = [['4', '2', '1', '3'], ['16', '4', '1', '3'], ['9', '3', '1', '2']]
mo.print_matrix(mo.RREF(G))
