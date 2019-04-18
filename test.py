import LA
mm = LA.Make_Matrix()
mo = LA.Matrix_Operations()
vo = LA.Vector_Operations()

x = mm.make_random_matrix(3, 1)
y = mm.make_random_matrix(3, 1)
z = mm.make_random_matrix(3, 1)
mo.print_matrix(x, y, z)
result = vo.scalar_triple_product(x, y, z)

print(result)
