import LA
mm = LA.Make_Matrix()
mo = LA.Matrix_Operations()
mv = LA.Make_Vector()
def test():
    random_matrix = mm.make_random_matrix(3, 4)
    mo.print_matrix_new(random_matrix)
    mo.print_matrix_new(mo.matrix_multiply_constant(random_matrix, 10))
    random_column_vector = mv.make_random_column_vector(3)
    random_row_vector = mv.make_random_row_vector(3)
    mo.print_matrix_new(random_column_vector)
    mo.print_matrix_new(random_row_vector)

def test2():
    m1 = mm.make_random_matrix(3, 3)
    m2 = mm.make_random_matrix(3, 3)
    mo.print_matrix_new(mo.matrix_multiply(m1, m2))

test2()
