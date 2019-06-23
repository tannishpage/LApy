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
import math
import datetime
import time

# Global Variables
AUTHOR = "Tannishpage"
GITHUB = "https://github.com/tannishpage"
LAPY_STABLE = "https://github.com/tannishpage/LApy/tree/Stable_Version"
LAPY_DEV = "https://github.com/tannishpage/LApy"
VERSION = "0.7"
DATE = str(datetime.datetime.date(datetime.datetime.now())).split("-")[0]
MESSAGE = """Author         :  {}
My Github      :  {}
LApy Stable    :  {}
LApy Dev       :  {}
LApy Version   :  {}


LApy  Copyright (C) {}  {}
This program comes with ABSOLUTELY NO WARRANTY; This is free software, 
and you are welcome to redistribute it under certain conditions; 
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
""".format(AUTHOR, GITHUB, LAPY_STABLE, LAPY_DEV, VERSION, 
           str(datetime.datetime.date(datetime.datetime.now())).split("-")[0],
           AUTHOR)

# Exceptions that are specific
class Zero_Determinant_Error(BaseException):pass
class Not_Compatable_Operation(BaseException):pass
class Incompatable_Matricies(BaseException):pass
class Invalid_Vectors(BaseException):pass
class Invalid_Parameter(BaseException):pass

class Matrix_Operations:
    """
    Contains all the functions that perform matrix operations 
    """
    def __init__(self):
        self._mm = Make_Matrix() # This makes it easier to make zero matricies
                                 # and stuff like that

    def matrix_add(self, *matricies):
        """
        Adds 2 or more matrices together
        Parameters:
            *matricies (Matrix): more then one matrices which are then 
                                 added together
        Return:test.p
            result (Matrix): returns the cumilative sum of all the given 
                             matrices
        """
        result = self._mm.make_zero_matrix(len(matricies[0]),
                                           len(matricies[0][0]))
        for matrix in matricies:
            for x in range(0, len(result)):
                for y in range(0, len(result[0])):
                    result[x][y] = str(float(result[x][y]) + float(matrix[x][y]))
        return result

    def matrix_subtract(self, matrixA, matrixB):
        """
        subtracts matrixB from matrixA
        Parameters:
            matrixA (Matrix): a n by m matrix
            matrixB (Matrix): a n by m matrix
        Return:
            result (Matrix): returns the result of matrixA - matrixB
        """
        result = matrixA
        for x in range(0, len(result)):
            for y in range(0, len(result[0])):
                result[x][y] = str(float(result[x][y]) - float(matrixB[x][y]))
        return result


    def matrix_multiply(self, matrixA, matrixB):
        """
        Multiplies matrixA and matrixB
        Parameters:
            matrixA (Matrix): a n by m matrix
            matrixB (Matrix): a n by m matrix
        Return:
            result (Matrix): returns the result of matrixA * matrixB
        """
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
        """
        Multiplies a matrix with a constant
        Parameters:
            matrix (Matrix): a n by m matrix
            constant (int): the scaler constant
        Return:
            result (Matrix): returns the result of matrixA * constant
        """
        result = self._mm.make_zero_matrix(len(matrix), len(matrix[0]))
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix[0])):
                result[x][y] = str(constant * float(matrix[x][y]))
        return result

    def REF(self, matrix):
        """
        Reduces a matrix into a upper triangular matrix
        
        Parameters:
            matrix (Matrix): a n by n matrix

        Return:
            matrix (Matrix): a n by n matrix reduced into an upper triangular
                             matrix
        """
        matrix = self.check_matrix_row_exchange(matrix)
        for x in range(0, len(matrix)):
            matrix = self.check_row_exchange(matrix, x)
            piviot = float(matrix[x][x])
            for y in range(x+1, len(matrix)):
                ratio = float(float(matrix[y][x])/piviot)
                matrix[y] = self.row_reduction(matrix[x], matrix[y], ratio)
        return matrix

    def get_last_column(self, matrix):#assuming matrix is NxN+1
        """
        Splits a matrix at its last column

        Parameters:
            matrix (Matrix): a n by m matrix (Preferably n by n+1)

        Return:
            last_column (list<list>): Contains the last column of the matrix
            square_matrix (Matrix): Is the matrix without its last column
        """
        last_column = Matrix()
        square_matrix = self._mm.make_zero_matrix(len(matrix), len(matrix))
        for x in range(0, len(matrix)):
            for y in range(0, len(matrix)):
                square_matrix[x][y] = matrix[x][y]
            last_column.append([matrix[x][len(matrix)]])
        return last_column, square_matrix

    def check_row_exchange(self, matrix, row):
        """
        Checks the matrix for row exchanges and performs the row exchange

        Parameters: 
            matrix (Matrix): a n by n matrix (Can be n by m where n != m)
            row (list): a row from matrix that is required to be checked

        Return:
            new_matrix (Matrix): The original matrix with the row exchanged
            matrix (Matrix): The original matrix with no row exchanged
        """
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
        """
        Performs a check on the entire matrix for row exchanges

        Parameters:
            matrix (Matrix): a n by n matrix (Can be n by m where n != m)
        
        Return:
            matrix (Matrix): original matrix, may or may not be modified
        """
        for x in range(0, len(matrix)):
            matrix = self.check_row_exchange(matrix, x)
        return matrix

    def perform_row_exchange(self, rowA, rowB, matrix):
        """
        Swaps rowA with rowB in matrix

        Parameters:
            rowA, rowB (int): is the index that points to two unique rows in matrix
            matrix (Matrix): is the matrix that the row exchange is performed on

        Return:
            matrix (Matrix): original matrix with the rows exchanged
        """
        rowA_list = matrix[rowA]
        rowB_list = matrix[rowB]
        matrix[rowA] = rowB_list
        matrix[rowB] = rowA_list
        return matrix

    def make_piviots_ones(self, matrix):
        """
        Makes all the piviots of the matrix 1 by dividing the piviot row by the piviot

        Parameters:
            matrix (Matrix): is a n by n matrix
        
        Return:
            matrix (Matrix): the original matrix with the piviots turned to ones
        """
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
        """
        An extention on REF. RREF turns the upper triangular matrix given by REF
        into the identity matrix.

        The input matrix can be non square, the REF and RREF functions will
        treat it as a square.

        Precondition:
            matrix dimentions must must be n by m
            where n <= m

        Parameters:
            matrix (Matrix): an n by n matrix
        
        Return:
            matrix (Matrix): still n by n matrix but reduced to an identity matrix 
        """
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
        """
        Function called by REF and RREF to perform row Reduction on matrix

        Parameters:
            piviot_row (list): is the piviot row in the matrix
            rowB (list): is the row being reduced
            ratio (float): is the ratio of num_below_piviot/piviot

        Return:
            reduced_row (list): is the row that contains rowB reduced by the piviot row
        """
        reduced_row = []
        for x in range(0, len(rowB)):
            reduced_row.append(str(float(float(rowB[x]) - (ratio*float(pivoit_row[x])))))
        return reduced_row

    def compute_determinant(self, matrix):
        """
        Computes the determinant of a matrix using the REF function and
        multiplying the diagonals of the reduced matrix.

        Precondition:
            matrix MUST be n by n i.e. square

        Parameters:
            matrix (Matrix): is an n by n matrix 

        Return:
            determinant (float): is the determinant of the matrix
        """
        reduced_matrix = self.REF(matrix)
        determinant = 1.0
        for x in range(0, len(reduced_matrix)):
            determinant = determinant * float(reduced_matrix[x][x])
        return determinant

    def matrix_transpose(self, matrix): #Transposes a matrix
        """matrix (Matrix) is transposed"""
        #Make a zero matrix the same size as the matrix
        result = self._mm.make_zero_matrix(len(matrix[0]), len(matrix))
        for x in range(0, len(result[0])):
            for y in range(0, len(result)):
                result[y][x] = matrix[x][y]
        return result

    def compute_inverse(self, matrix, identity):#transform into augmented matrix
        """
        Computes the inverse of matrix using the Gaussian Elimination method

        Precondition:
            matrix MUST be n by n i.e. square

        Parameters:
            matrix (Matrix): an n by n matrix
            identity (Matrix): an n by n matrix which is the Identity matrix
        
        Return:
            (Matrix): The inverse matrix of the original matrix
        """
        augmented = self.join_matricies(matrix, identity)
        determinant = self.compute_determinant(augmented)
        if determinant == 0:
            raise Zero_Determinant_Error(
            "Matrix Inverse does not exist when determinant is 0")
        else:
            inverse = self.RREF(augmented)
            return self.split_matrix(inverse, int(len(inverse[0])/2))

    def split_matrix(self, matrix, start):
        """
        Splits a matrix from the index start (Used by compute inverse to
        split the augmented matrix into a regular n by n matrix with the 
        inverse)

        Paramenters:
            matrix (Matrix): n by m matrix
            start (int): the index at which the splitting should begin

        Return:
            result (Matrix): is the resulting matrix after the split
        """
        result = self._mm.make_zero_matrix(len(matrix), start)
        for x in range(0, len(matrix)):
            for y in range(0, start):
                result[x][y] = matrix[x][y+start]
        return result

    def mcp(self, matrix):
        """
        Copies matrix into another matrix (instead of passing by reference)

        Parameters: 
            matrix (Matrix): is the matrix to be copied
        
        Return:
            copy (Matrix): is a copy of matrix (not pass by reference)
        """
        #Copies matrix into a new matrix wihout being passed as a reference
        pass
        
    def join_matricies(self, matrixA, matrixB):
        """
        Joins two matrices together (Used in compute_inverse to augment
        the matrix and the identity matrix)

        Precondition:
            matrixA and matrixB must have the same number of rows

        Parameters: 
            matrixA (Matrix): an n by m matrix
            matrixB (Matirx): an n by o matrix

        Return:
            big_matrix (Matrix): n by m+o matrix consisting of both matrixA and
            matrixB
        """
        big_matrix = self._mm.make_zero_matrix(len(matrixA), 
                                        len(matrixA[0])+len(matrixB[0]))
        for x in range(0, len(big_matrix)):
            for y in range(0, len(matrixA[0])):
                big_matrix[x][y] = matrixA[x][y]
                big_matrix[x][y+(len(matrixA[0]))] = matrixB[x][y]
        return big_matrix

    def print_matrix(self, *matricies, padding=12, sigfig=2):
        """
        Prints out the matrices given in a formated way

        Parameters:
            *matricies (list<Matrix>): is a list of matricies that are printed
            out one after the other

            padding (int): is the amount of padding to be used between the
            elements in the matrix when prited out

            sigfig (int): is the number of significant figures to be displayed
            when the elements are printed out
        """
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
    """
    Is a class used to generate different kinds of matricies and vectors
    """

    def make_matrix(self):
        """(Matirx) lets the user make a matrix"""
        rows = int(input("Enter number of rows: "))
        matrix = []
        for x in range(0, rows):
            row_values = input("Enter numbers in row {} (eg: 1 2 3) : ".format(x+1))
            matrix.append(row_values.split(" "))
        return Matrix(matrix)

    def make_random_matrix(self, rows, columns):
        """(Matrix) generates a random matrix of size rows and columns"""
        matrix = []
        for x in range(0, rows):
            row_values = [str(random.randint(0, 5)) for x in range(0, columns)]
            matrix.append(row_values)
        return Matrix(matrix)

    def make_zero_matrix(self, rows, columns):
        """(Matrix) generates a zero matrix of size rows and columns"""
        matrix = []
        for x in range(0, rows):
            column = ["0" for x in range(0, columns)]
            matrix.append(column)
        return Matrix(matrix)

    def make_identity_matrix(self, rows):
        """(Matrix) generates an indentity matrix of size rows by rows"""
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
        """(bool) checks if the vector is a column vector"""
        if (len(self._matrix) > 1 and len(self._matrix[0]) == 1):
            return True
        else:
            return False

    def is_row(self):
        """(bool) checks if the vector is a row vector"""
        if len(self._matrix) == 1:
            return True
        else:
            return False


class Vector_Operations:
    """
    Contains all the methods that perform vector operations
    """
    def __init__(self):
        # Making an object for Make_Matrix and Matrix_Operations
        self._mm = Make_Matrix()
        self._mo = Matrix_Operations()

    def vector_dot_product(self, vectorA, vectorB):
        """
        Calculates the dot product of VectorA and VectorB

        Precondition:
            vectorA and vectorB must be column vectors
            dot product isn't implimented for row vectors

        Parameters:
            vectorA, vectorB (Matrix): is a column vector (or a n by 1 matrix)
        
        Return:
            result (float): The dot product of vectorA and vectorB
        """
        if not vectorA.is_column() or not vectorB.is_column():
            raise Invalid_Vectors("Vector A or B are not column vectors")

        result = 0
        for x in range(0, len(vectorA)):
            result = result + (float(vectorA[x][0]) * float(vectorB[x][0]))
        return result

    def vector_cross_product(self, vectorA, vectorB):
        """ 
        Calculates the cross product of vectorA and vectorB

        Precondition:
            vectorA, vectorB must be column vectors and of size 3
            or they must be vectors in R^3
        
        Parameters:
            vectorA, vectorB (Matrix): is a column vector (or a n by 1 matrix)
        
        Return:
            result (Matrix): is a column vector of size 3, and is the cross
            product of vectorA and vectorB
        """
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
        """
        Calculates the magnitude of the vectorA

        Precondition:
            vectorA must be a column vector

        Parameters:
            vectrorA (Matrix): is a column vector (or a n by 1 matrix)

        Return:
            magnitude (float): the magnitude of the vectorA 
        """
        magnitude = self.vector_dot_product(vectorA, vectorA)**0.5
        return magnitude

    def scalar_triple_product(self, vectorA, vectorB, vectorC):
        """
        calculates the scalar triple product of vectorA B and C

        Precondition:
            vectorA, B and C must be column vectors
        
        Parameters:
            vectorA, vectorB, vectorC (Matrix): is a column vector (or a n by 1 matrix)
        
        Return:
            (float): the scalar triple product of vectorA, B and C
        """
        if not vectorA.is_column() or not vectorB.is_column or not vectorC.is_column:
            raise Invalid_Vectors("Vector A, B or C are not column vectors")
        if len(vectorA) != 3 or len(vectorB) != 3 or len(vectorC) != 3:
            raise Invalid_Vectors("Vector A, B or C are not in R^3")

        result = self.vector_cross_product(vectorB, vectorC)
        return self.vector_dot_product(vectorA, result)

    def get_angle_between(self, vectorA, vectorB, units="rad"):
        """
        Calculates the angle between two vectors A and B.

        Precondition:
            vectorA, B must be column vectors

        Parameters:
            vectorA, vectorB (Matrix): is a column vector (or a n by 1 matrix)
            units (str): Default "rad", determins what units the output will be
            in. Radians or degrees "rad" or "deg"
        """
        #theta = arcsin(a.b/|a||b|)
        dot_product = self.vector_dot_product(vectorA, vectorB)
        magA = self.vector_magnitude(vectorA)
        magB = self.vector_magnitude(vectorB)
        angle = math.acos(dot_product/(magA * magB))
        if units.lower() == 'rad':
            return angle
        elif units.lower() == 'deg':
            return math.degrees(angle)
        else:
            raise Invalid_Parameter("\"{}\" is not a recognised unit. \
                  Only rad or deg. Default is rad.".format(units))
        
    def get_angle_between_horizontal(self, vectorA, units="rad"):
        """
        Calculates the angle between two vectorA and the horizontal (the x axis).

        Precondition:
            vectorA must be column vector in R^2

        Parameters:
            vectorA (Matrix): is a column vector in R^2 (or a 2 by 1 matrix)
            units (str): Default "rad", determins what units the output will be
            in. Radians or degrees "rad" or "deg"
        """
        mag = self.vector_magnitude(vectorA)
        angle = math.acos(float(vectorA[0][0])/mag)
        if units.lower() == 'rad':
            return angle
        elif units.lower() == 'deg':
            return math.degrees(angle)
        else:
            raise Invalid_Parameter("\"{}\" is not a recognised unit. \
                  Only rad or deg. Default is rad.".format(units))

if __name__ == "__main__":
    for x in MESSAGE:
        sys.stdout.write(x)
        sys.stdout.flush()
        time.sleep(0.03)
