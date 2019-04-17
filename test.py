import LA
mm = LA.Make_Matrix()
mo = LA.Matrix_Operations()
vo = LA.Vector_Operations()

x = mm.make_random_matrix(3, 1)
mo.print_matrix(x)
y = mm.make_random_matrix(3, 1)
mo.print_matrix(mo.matrix_transpose(y))

#mo.print_matrix()
