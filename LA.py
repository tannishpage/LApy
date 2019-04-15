"""
                        LICENSE

This is LApy a Linear Algebra API made with python.
Copyright (C) 2019  Tannishpage

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# Libraries required
import random
import sys

# Global Variables
AUTHOR = "Tannishpage"
GITHUB = "https://github.com/tannishpage"
LAPY_STABLE = "https://github.com/tannishpage/LApy/tree/Stable_Version"
LAPY_DEV = "https://github.com/tannishpage/LApy"
VERSION = "0.6"

# Exceptions that are specific
class Zero_Determinant_Error(BaseException):pass
class Not_Compatable_Operation(BaseException):pass
class Incompatable_Matricies(BaseException):pass

class Matrix_Operations:

    def __init__(self):
        self._mm = Make_Matrix()

    def matrix_add(self, matricies):
        result = matricies[0]
        for matrix in matricies[1::]:
            for x in range(0, len(result)):
                for y in range(0, len(result[0])):
                    result[x][y] = str(int(result[x][y]) + int(matrix[x][y]))
        return result

    def matrix_subtract(self, matricies):
        result = matricies[0]
        for matrix in matricies[1::]:
            for x in range(0, len(result)):
                for y in range(0, len(result[0])):
                    result[x][y] = str(int(result[x][y]) - int(matrix[x][y]))
        return result

    def matrix_multiply(self, matrixA, matrixB):
        if len(matrixA[0]) != len(matrixB):
            raise Incompatable_Matricies(
            "Matrix A columns not equal to Matrix B rows {} != {}".format(
            len(matrixA[0]), len(matrixB)))

        result = self._mm.make_zero_matrix(len(matrixA), len(matrixB[0]))
        temp_result = 0
        for x in range(0, len(matrixA)):
            for y in range(0, len(matrixA)):
                for z in range(0, len(matrixA)):
                    temp_result = temp_result + (int(matrixA[x][z]) * int(matrixB[z][y]))
                else:
                    result[x][y] = str(temp_result)
                    temp_result = 0
        return result

    def matrix_multiply_constant(self, matrix, constant):
        result = self._mm.make_zero_matrix(len(matrix), len(matrix[0]))
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix[0])):
                result[x][y] = str(constant * int(matrix[x][y]))
        return result

    def REF(self, matrix):
        matrix = self.check_matrix_row_exchange(matrix)
        for x in range(0, len(matrix)):
            matrix = self.check_row_exchange(matrix, x)
            piviot = float(matrix[x][x])
            for y in range(x+1, len(matrix)):
                ratio = float(float(matrix[y][x])/piviot)
                matrix[y] = self.row_reduction(matrix[x], matrix[y], ratio)
        return matrix

    def get_last_column(self, matrix):#assuming matrix is NxN+1
        last_column = []
        square_matrix = self._mm.make_zero_matrix(len(matrix), len(matrix))
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix)):
                square_matrix[x][y] = matrix[x][y]
            last_column.append(matrix[x][len(matrix)])
        return last_column, square_matrix

    def check_row_exchange(self, matrix, row):
        if float(matrix[row][row]) == 0.0:
            for x in range(0, len(matrix)):
                if (float(matrix[x][row]) != 0.0):
                    rowB = x
                    break
            new_matrix = self.perform_row_exchange(row, rowB, matrix)
            return new_matrix
        else:
            return matrix

    def check_matrix_row_exchange(self, matrix):
        for x in range(0, len(matrix)):
            matrix = self.check_row_exchange(matrix, x)
        return matrix

    def perform_row_exchange(self, rowA, rowB, matrix):
        rowA_list = matrix[rowA]
        rowB_list = matrix[rowB]
        matrix[rowA] = rowB_list
        matrix[rowB] = rowA_list
        return matrix

    def make_piviots_ones(self, matrix):
        new_matrix = []
        for x in range(0, len(matrix)):
            piviot = matrix[x][x]
            row = []
            for y in matrix[x]:
                row.append(str(float(float(y)/float(piviot))))
            else:
                new_matrix.append(row)
        return new_matrix

    def RREF(self, matrix):
        matrix = self.REF(matrix) #reduced to Row Echolon Form
        #now performs elimination to make it into Reduced REF
        matrix = self.check_matrix_row_exchange(matrix)
        matrix = self.make_piviots_ones(matrix) #makes all piviots into 1s
        for x in range(0, len(matrix))[::-1]:
            #matrix = self.check_row_exchange(matrix, x)
            piviot = float(matrix[x][x])
            for y in range(0, x)[::-1]:
                ratio = float(float(matrix[y][x])/piviot)
                matrix[y] = self.row_reduction(matrix[x], matrix[y], ratio)
        return matrix

    def row_reduction(self, pivoit_row, rowB, ratio):
        reduced_row = []
        for x in range(0, len(rowB)):
            reduced_row.append(str(float(float(rowB[x]) - (ratio*float(pivoit_row[x])))))
        return reduced_row

    def compute_determinant(self, matrix):
        reduced_matrix = self.REF(matrix)
        determinant = 1.0
        for x in range(0, len(reduced_matrix)):
            determinant = determinant * float(reduced_matrix[x][x])
        return determinant

    def matrix_transpose(self, matrix): #Transposes a matrix
        #Make a zero matrix the same size as the matrix
        result = self._mm.make_zero_matrix(len(matrix[0]), len(matrix))
        for x in range(0, len(result[0])):
            for y in range(0, len(result)):
                result[y][x] = matrix[x][y]
        return result

    def compute_inverse(self, matrix, identity):#transform into augmented matrix
        augmented = self.join_matricies(matrix, identity)
        determinant = self.compute_determinant(augmented)
        if determinant == 0:
            raise Zero_Determinant_Error(
            "Matrix Inverse does not exist when determinant is 0")
        else:
            return self.RREF(augmented) 
        
    def join_matricies(self, matrixA, matrixB):
            big_matrix = self._mm.make_zero_matrix(len(matrixA), 
                                          len(matrixA[0])+len(matrixB[0]))
            for x in range(0, len(big_matrix)):
                for y in range(0, len(matrixA[0])):
                    big_matrix[x][y] = matrixA[x][y]
                    big_matrix[x][y+(len(matrixA[0]))] = matrixB[x][y]
            return big_matrix

    def print_matrix(self, matrix):
        for row in matrix:
            print("    ".join(row))
        else:
            print("\n")
        return True

    def print_matrix_new(self, matrix):
        for row in matrix:
            for element in row:
                sys.stdout.write("{:<10}".format("{:.4f}".format(float(element))))
            else:
                sys.stdout.write("\n")
        else:
            print("\n")

class Make_Matrix:
    # A matrix is defiend as a two dimentional list
    def __init__(self):
        pass

    def make_matrix(self):
        rows = int(input("Enter number of rows: "))
        matrix = []
        for x in range(0, rows):
            row_values = input("Enter numbers in row {} (eg: 1 2 3) : ".format(x+1))
            matrix.append(row_values.split(" "))
        return matrix

    def make_random_matrix(self, rows, columns):
        matrix = []
        for x in range(0, rows):
            row_values = [str(random.randint(0, 100)) for x in range(0, columns)]
            matrix.append(row_values)
        return Matrix(matrix)

    def make_zero_matrix(self, rows, columns):
        matrix = []
        for x in range(0, rows):
            column = ["0" for x in range(0, columns)]
            matrix.append(column)
        return matrix

    def make_identity_matrix(self, rows):
        matrix = self.make_zero_matrix(rows, rows)
        for x in range(0, rows):
            matrix[x][x] = "1"
        return matrix

class Matrix:
    def __init__(self, matrix=[]):
        self._matrix = matrix

    def __iter__(self):
        return iter(self._matrix)

    def __len__(self):
        return len(self._matrix)

    def __repr__(self):
        return "Matrix({})".format(self._matrix)

    def __str__(self):
        return "{}".format(self._matrix)

    def __getitem__(self, args):
        return self._matrix[args]


class Vector_Operations:
    def __init__(self):
        self._mv = Make_Vector()

    def vector_add(self, vectors):
        result = self._mv.make_zero_vector(self, len(vectors[0]))
        for vector in vectors:
            for x in range(0, len(vector)):
                result[x] = str(float(result[x]) + float(vector[x]))
        return result

    def vector_subtract(self, vectorA, vectorB):
        result = self._mv.make_zero_vector(self, len(vectorA))
        for x in range(0, len(vectorA)):
            result[x] = str(float(vectorA[x]) - float(vectorB[x]))
        return result

    def vector_cross_product(self, vectorA, vectorB):
       """
        - Is vector cross product valid for len(vector) > 3 and len(vector) < 3?
       """
       # matrixA = 
       # matrixB = 
       # matrixC =
       pass

    def vector_dot_product(self, vectorA, vectorB):
        result = 0
        for x in range(0, len(vectorA)):
            result = result + (float(vectorA[x]) * float(vectorB[x]))
        return result
            

class Make_Vector:
    def __init__(self):
        pass

    def make_coloumn_vector(self):
        vector_values = input("Enter vector values (eg: 1 2 3): ").split(" ")
        vector = []
        length = len(vector_values)
        for x in range(0, len(vector_values)):
            vector.append([vector_values[x]])
        return Vector(vector)

    def make_zero_column_vector(self, size):
        vector = []
        for x in range(0, size):
            vector.append(["0"])
        return Vector(vector)

    def make_random_column_vector(self, size):
        vector = []
        for x in range(0, size):
            vector.append([str(random.randint(0, 9))])
        return Vector(vector)

    def make_row_vector(self):
        vector_values = input("Enter vector values (eg: 1 2 3): ")
        vector = vector_values.split(" ")
        return Vector([vector])

    def make_zero_row_vector(self, size):
        return Vector([["0" for x in range(0, size)]])

    def make_random_row_vector(self, size):
        return Vector([[str(random.randint(0, 9)) for x in range(0, size)]])

class Vector:
    
    def __init__(self, vector=[]):
        self._vector = vector

    def __iter__(self):
        return iter(self._vector)

    def __len__(self):
        return len(self._vector)

    def __repr__(self):
        return "Vector({})".format(self._vector)

    def __str__(self):
        return "{}".format(self._vector)

    def __getitem__(self, args):
        return self._vector[args]

    def is_column(self):
        if len(self._vector) > 1:
            return True
        else:
            return False

    def is_row(self):
        if len(self._vector) == 1:
            return True
        else:
            return False

if __name__ == "__main__":
    print("""Author         :  {}
My Github      :  {}
LApy Stable    :  {}
LApy Dev       :  {}
LApy Version   :  {}
""".format(AUTHOR, GITHUB, LAPY_STABLE, LAPY_DEV, VERSION))
