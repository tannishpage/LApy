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
class Invalid_Vectors(BaseException):pass

class Matrix_Operations:

    def __init__(self):
        self._mm = Make_Matrix()

    def matrix_add(self, *matricies):
        result = self._mm.make_zero_matrix(len(matricies[0]), len(matricies[0][0]))
        for matrix in matricies:
            for x in range(0, len(result)):
                for y in range(0, len(result[0])):
                    result[x][y] = str(float(result[x][y]) + float(matrix[x][y]))
        return result

    def matrix_subtract(self, matrixA, matrixB):
        result = matrixA
        for x in range(0, len(result)):
            for y in range(0, len(result[0])):
                result[x][y] = str(float(result[x][y]) - float(matrixB[x][y]))
        return result


    def matrix_multiply(self, matrixA, matrixB):
        if len(matrixA[0]) != len(matrixB):
            raise Incompatable_Matricies(
            "Matrix A columns not equal to Matrix B rows {} != {}".format(
            len(matrixA[0]), len(matrixB)))

        result = self._mm.make_zero_matrix(len(matrixA), len(matrixB[0]))
        temp_result = 0
        for x in range(0, len(matrixA)):
            for y in range(0, len(matrixB[0])):
                for z in range(0, len(matrixA[0])):
                    temp_result = temp_result + (float(matrixA[x][z]) * float(matrixB[z][y]))
                else:
                    result[x][y] = str(temp_result)
                    temp_result = 0
        return result

    def matrix_multiply_constant(self, matrix, constant):
        result = self._mm.make_zero_matrix(len(matrix), len(matrix[0]))
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix[0])):
                result[x][y] = str(constant * float(matrix[x][y]))
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
        last_column = Matrix()
        square_matrix = self._mm.make_zero_matrix(len(matrix), len(matrix))
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix)):
                square_matrix[x][y] = matrix[x][y]
            last_column.append([matrix[x][len(matrix)]])
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
        return Matrix(new_matrix)

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
        return Matrix(matrix)

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
        return Matrix(result)

    def compute_inverse(self, matrix, identity):#transform into augmented matrix
        augmented = self.join_matricies(matrix, identity)
        determinant = self.compute_determinant(augmented)
        if determinant == 0:
            raise Zero_Determinant_Error(
            "Matrix Inverse does not exist when determinant is 0")
        else:
            inverse = self.RREF(augmented)
            return self.split_matrix(inverse, int(len(inverse[0])/2))

    def split_matrix(self, matrix, start):
        result = self._mm.make_zero_matrix(len(matrix), start)
        for x in range(0, len(matrix)):
            for y in range(0, start):
                result[x][y] = matrix[x][y+start]
        return result

    def mcp(zero_matrix, matrix):
        #Copies matrix into a new matrix wihout being passed as a reference
        pass
        
    def join_matricies(self, matrixA, matrixB):
            big_matrix = self._mm.make_zero_matrix(len(matrixA), 
                                          len(matrixA[0])+len(matrixB[0]))
            for x in range(0, len(big_matrix)):
                for y in range(0, len(matrixA[0])):
                    big_matrix[x][y] = matrixA[x][y]
                    big_matrix[x][y+(len(matrixA[0]))] = matrixB[x][y]
            return big_matrix

    def print_matrix(self, *matricies, padding=12, sigfig=2):
        for matrix in matricies:
            for row in matrix:
                for element in row:
                    sys.stdout.write("{:<{}}".format("{:.{}f}".format(
                                              float(element), sigfig), padding))
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
        return Matrix(matrix)

    def make_random_matrix(self, rows, columns):
        matrix = []
        for x in range(0, rows):
            row_values = [str(random.randint(0, 5)) for x in range(0, columns)]
            matrix.append(row_values)
        return Matrix(matrix)

    def make_zero_matrix(self, rows, columns):
        matrix = []
        for x in range(0, rows):
            column = ["0" for x in range(0, columns)]
            matrix.append(column)
        return Matrix(matrix)

    def make_identity_matrix(self, rows):
        matrix = self.make_zero_matrix(rows, rows)
        for x in range(0, rows):
            matrix[x][x] = "1"
        return Matrix(matrix)

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

    def __getitem__(self, key):
        return self._matrix[key]

    def __setitem__(self, key, value):
        self._matrix[key] = value

    def append(self, value):
        self._matrix.append(value)

    def is_column(self):
        if (len(self._matrix) > 1 and len(self._matrix[0]) == 1):
            return True
        else:
            return False

    def is_row(self):
        if len(self._matrix) == 1:
            return True
        else:
            return False


class Vector_Operations:
    def __init__(self):
        self._mm = Make_Matrix()
        self._mo = Matrix_Operations()

    def vector_dot_product(self, vectorA, vectorB):
        if not vectorA.is_column() or not vectorB.is_column():
            raise Invalid_Vectors("Vector A or B are not column vectors")

        result = 0
        for x in range(0, len(vectorA)):
            result = result + (float(vectorA[x][0]) * float(vectorB[x][0]))
        return result

    def vector_cross_product(self, vectorA, vectorB):
        if not vectorA.is_column() or not vectorB.is_column():
            raise Invalid_Vectors("Vector A or B are not column vectors")
        if len(vectorA) != 3 or len(vectorB) != 3:
            raise Invalid_Vectors("Vector A or B are not in R^3")

        result = self._mm.make_zero_matrix(3, 1)
        result[0][0] = str((float(vectorA[1][0]) * float(vectorB[2][0])) - 
                           (float(vectorA[2][0]) * float(vectorB[1][0])))

        result[1][0] = str((float(vectorA[2][0]) * float(vectorB[0][0])) - 
                           (float(vectorA[0][0]) * float(vectorB[2][0])))

        result[2][0] = str((float(vectorA[0][0]) * float(vectorB[1][0])) - 
                           (float(vectorA[1][0]) * float(vectorB[0][0])))
        return result

    def vector_magnitude(self, vectorA):
        magnitude = self.vector_dot_product(vectorA, vectorA)**0.5
        return magnitude

    def scalar_triple_product(self, vectorA, vectorB, vectorC):
        if not vectorA.is_column() or not vectorB.is_column or not vectorC.is_column:
            raise Invalid_Vectors("Vector A, B or C are not column vectors")
        if len(vectorA) != 3 or len(vectorB) != 3 or len(vectorC) != 3:
            raise Invalid_Vectors("Vector A, B or C are not in R^3")

        result = self.vector_cross_product(vectorB, vectorC)
        return self.vector_dot_product(vectorA, result)

if __name__ == "__main__":
    print("""Author         :  {}
My Github      :  {}
LApy Stable    :  {}
LApy Dev       :  {}
LApy Version   :  {}
""".format(AUTHOR, GITHUB, LAPY_STABLE, LAPY_DEV, VERSION))
