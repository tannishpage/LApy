import LA
mm = LA.Make_Matrix()
mo = LA.Matrix_Operations()
mv = LA.Make_Vector()
vo = LA.Vector_Operations()

def test():
    m1 = mm.make_random_matrix(2, 2)
    i = mm.make_identity_matrix(2)
    vec_r = mv.make_random_column_vector(2)
    vec_ans = mv.make_zero_column_vector(2)
    mo.print_matrix_new(m1)
    mo.print_matrix_new(i)
    mo.print_matrix_new(vec_r)
    mo.print_matrix_new(vec_ans)
    mo.print_matrix_new(mo.compute_inverse(m1, i))
    vec_ans = mo.matrix_multiply(mo.compute_inverse(m1, i), vec_r)
    mo.print_matrix_new(vec_ans)    

test()
