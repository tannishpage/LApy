import LA
mm = LA.Make_Matrix()
mo = LA.Matrix_Operations()
vo = LA.Vector_Operations()

x = mm.make_random_matrix(100, 100)
mo.print_matrix(x)
inverse = mo.compute_inverse(x, mm.make_identity_matrix(100))
mo.print_matrix(inverse)
