import LA
mm = LA.Make_Matrix()
mo = LA.Matrix_Operations()
vo = LA.Vector_Operations()

def test():
    vector1 = mm.make_random_matrix(3, 1)
    vector2 = mm.make_random_matrix(3, 1)
    mo.print_matrix(vector1, vector2, mo.matrix_add(vector1, vector2))

test()
