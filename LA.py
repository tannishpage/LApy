'''
Plan:
    This is supposed to be an api for Linear Algebra so it is supposed to perform matrix opperations and other vector operations like dot products and cross products.

Basic Functionality:
    - Add and Subtract matricies DONE
    - Multiply Matricies DONE
    - Compute Determinants DONE
    - Compute Inverses DONE


TO-DO-LIST:
    1. Finish make_zero_matrix DONE
    2. Test matrix_add DONE
    3. Make matrix_sub DONE 
    4. Make matrix_multiply DONE
    5. Get print_matrix to have good formatting cause it sucks at the moment :) DONE
    6. Multiply matricies by constants
'''
import random
import sys
class matrix_opperations:

    def __init__(self, VERSION="0.5"):
        self.VERSION = "0.5"

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

    def REF(self, matrix): #, augmented_column):#assume no row exchanges are required
        matrix = self.check_matrix_row_exchange(matrix)
        #matrix_duplicate = matrix
        #aug_col_duplicate = augmented_column
        for x in range(0, len(matrix)):
            matrix = self.check_row_exchange(matrix, x)
            piviot = float(matrix[x][x])
            for y in range(x+1, len(matrix)):
                ratio = float(float(matrix[y][x])/piviot)
                matrix[y] = self.row_reduction(matrix[x], matrix[y], ratio)
                #augmented_column[y] = self.row_reduction(augmented_column[x], augmented_column[y], ratio) 
        return matrix#, augmented_column

    def get_last_column(self, matrix):#assuming matrix is NxN+1
        last_column = []
        square_matrix = make_matrix.make_zero_matrix(self, len(matrix), len(matrix))
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix)):
                square_matrix[x][y] = matrix[x][y]
            last_column.append(matrix[x][len(matrix)])
        return last_column, square_matrix

    def check_row_exchange(self, matrix, row):
        if float(matrix[row][row]) == 0.0:
            for x in range(0, len(matrix)):
                if float(matrix[x][row]) != 0.0:
                    rowB = x
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
        result = make_matrix.make_zero_matrix(self, len(matrix), len(matrix[0])) #Make a zero matrix the same size as the matrix
        for x in range(0, len(result[0])):
            for y in range(0, len(result)):
                result[y][x] = matrix[x][y]
        return result

    def compute_inverse(self, matrix, identity):#transform into augmented matrix
        augmented = self.join_matricies(matrix, identity)
        determinant = self.compute_determinant(augmented)
        if determinant == 0:
            print("Determinant is 0 cannot compute inverse")
            return False
        else:
            return self.RREF(augmented) 
        
    def join_matricies(self, matrixA, matrixB):
            big_matrix = make_matrix.make_zero_matrix(self, len(matrixA), len(matrixA[0])+len(matrixB[0]))
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

class make_matrix:

    def __init__(self, VERSION="0.5"):
        self.VERSION = "0.5"

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
