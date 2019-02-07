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

    def REF(self, matrix, augmented_column):#assume no row exchanges are required
        #matrix = self.check_row_exchange(matrix, 0)
        matrix_duplicate = matrix
        aug_col_duplicate = augmented_column
        for x in range(0, len(matrix)):
            piviot = float(matrix[x][x])
            for y in range(x+1, len(matrix[0])):
                ratio = float(float(matrix[y][x])/piviot)
                matrix_duplicate[y] = self.row_reduction(matrix_duplicate[x], matrix_duplicate[y], ratio)
                aug_col_duplicate[y] = self.row_reduction(aug_col_duplicate[x], aug_col_duplicate[y], ratio) 
            #matrix_duplicate = self.check_matrix_row_exchange(matrix_duplicate)
        return matrix_duplicate, aug_col_duplicate

    def get_last_column(self, matrix):#assuming matrix is NxN+1
        last_column = []
        square_matrix = make_matrix.make_zero_matrix(self, len(matrix), len(matrix))
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix)):
                square_matrix[x][y] = matrix[x][y]
            last_column.append(matrix[x][len(matrix)])
        return last_column, square_matrix

    def check_row_exchange(self, matrix, row):
        if matrix[row][row] == "0":
            rowB = row + 1
            new_matrix = self.perform_row_exchange(row, rowB, matrix)
            return new_matrix
        else:
            return matrix

    def check_matrix_row_exchange(self, matrix):
        new_matrix = []
        for x in range(0, len(matrix)):
            new_matrix = self.check_row_exchange(matrix, x)
        return new_matrix

    def perform_row_exchange(self, rowA, rowB, matrix):
        rowA_list = matrix[rowA]
        rowB_list = matrix[rowB]
        matrix[rowA] = rowB_list
        matrix[rowB] = rowA_list
        return matrix
            

    def RREF(self, matrix):
        pass

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
        result = make_matrix.make_zero_matrix(self, len(matrix), len(matrix[0])) #Make a zero matrix the same size as the matrix
        for x in range(0, len(result[0])):
            for y in range(0, len(result)):
                result[y][x] = matrix[x][y]
        return result

    def compute_inverse(self, matrix):#transform into augmented matrix
        determinant = self.compute_determinant(matrix)
        identity = make_matrix.make_identity_matrix(len(matrix))
        if determinant == 0:
            print("Determinant is 0 cannot compute inverse")
            return False
        else:
            print("Still in development")
        
        
    def make_augmented_matrix(self, matrix):
        real_matrix = make_matrix.make_zero_matrix(len(matrix[0])/2, len(matrix[0])/2) #Must always be a square matrix
        augmented_matrix = make_matrix.make_zero_matrix(len(matrix[0])/2, len(matrix[0])/2) #Both real and augmented matrix must be same size
        for x in range(0, len(matrix[0]/2)):
            for y in range(0, len(matrix[0]/2)):
                real_matrix[x][y] = matrix[x][y]
                augmented_matrix[x][y] = matrix[x][len(matrix[0]/2) + y]
        return real_matrix, augmented_matrix
            

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
            row_values = [str(random.randint(0, 9)) for x in range(0, columns)]
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
