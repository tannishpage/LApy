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
for x in range(0, 1):
	a = mm.make_random_matrix(1000, 1001)#Matrix([["3", "5", "1"],["2", "9", "-4"],["-6", "2", "-9"]])
	#mo.print_matrix(a)
	mo.print_matrix(mo.RREF(a))
#b = #Matrix([["1", "1", "1"],["2", "3", "4"],["6", "5", "6"]])
#c = a + b
