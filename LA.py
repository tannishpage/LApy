'''
Plan:
    This is supposed to be an api for Linear Algebra so it is supposed to perform matrix opperations and other vector operations like dot products and cross products.

Basic Functionality:
    - Add and Subtract matricies DONE
    - Multiply Matricies DONE
    - Compute Determinants DONE
    - Compute Inverses


TO-DO-LIST:
    1. Finish make_zero_matrix DONE
    2. Test matrix_add DONE
    3. Make matrix_sub DONE 
    4. Make matrix_multiply DONE
    5. Get print_matrix to have good formatting cause it sucks at the moment :)
'''
import random
class matrix_opperations:

    def __init__(self, VERSION="0.1"):
        self.VERSION = "0.1"

    def matrix_add(self, matricies):
        result = matricies[0] #LA.make_matrix.make_zero_matrix(len(mm[1]), len(mm[1][1]))
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
        result = make_matrix.make_zero_matrix(self, len(matrixA), len(matrixB[0]))
        temp_result = 0
        for x in range(0, len(matrixA)):
            for y in range(0, len(matrixA)):
                for z in range(0, len(matrixA)):
                    temp_result = temp_result + (int(matrixA[x][z]) * int(matrixB[z][y]))
                else:
                    result[x][y] = str(temp_result)
                    temp_result = 0
        return result

    def REF(self, matrix): #For now assuming all matricies passed are square and don't require any row exchanges
        matrix_duplicate = matrix
        for x in range(0, len(matrix)):
            piviot = float(matrix[x][x])
            for y in range(x+1, len(matrix[0])):
                ratio = float(float(matrix[y][x])/piviot)
                matrix_duplicate[y] = self.row_reduction(matrix[x], matrix[y], ratio)
        return matrix_duplicate

    def row_reduction(self, pivoit_row, rowB, ratio):
        reduced_row = []
        for x in range(0, len(rowB)):
            reduced_row.append(str(int(float(rowB[x]) - (ratio*float(pivoit_row[x])))))
        return reduced_row

    def compute_determinant(self, matrix):
        reduced_matrix = self.REF(matrix)
        determinant = 1.0
        for x in range(0, len(reduced_matrix)):
            determinant = determinant * float(reduced_matrix[x][x])
        return determinant

    def matrix_transpose(self, matrix): #Transposes a matrix
        result = make_matrix.make_zero_matrix(self, len(matrix), len(matrix[0])) #Make a zero matrix the same size as the matrix
        for x in range(0, len(result[0])):
            for y in range(0, len(result)):
                result[y][x] = matrix[x][y]
        return result

    def print_matrix(self, matrix):
        for row in matrix:
            print("    ".join(row))
        else:
            print("\n")
        return True

class make_matrix:

    def __init__(self, VERSION="0.1"):
        self.VERSION = "0.1"

    def make_matrix(self):
        rows = int(input("Enter number of rows: "))
        matrix = []
        for x in range(0, rows):
            row_values = input("Enter numbers in row {} (eg: 1,2) : ".format(x+1))
            matrix.append(row_values.split(","))
        return matrix

    def make_random_matrix(self, rows, columns):
        matrix = []
        for x in range(0, rows):
            row_values = [str(random.randint(0, 100)) for x in range(0, columns)]
            matrix.append(row_values)
        return matrix

    def make_zero_matrix(self, rows, columns):
        matrix = []
        for x in range(0, rows):
            column = ("0,"*columns).split(',')
            del column[len(column)-1]
            matrix.append(column)
        return matrix

    def make_identity_matrix(self, rows):
        matrix = self.make_zero_matrix(rows, rows)
        for x in range(0, rows):
            matrix[x][x] = "1"
        return matrix
