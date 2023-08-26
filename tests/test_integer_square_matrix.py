import pytest
from matrix.square.integer.base import IntegerSquareMatrix


class TestIntegerSquareMatrix:
    def test_identity(self):
        size = 3
        matrix = IntegerSquareMatrix.identity(size)
        expected = IntegerSquareMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        assert matrix == expected

    def test_copy(self):
        original = IntegerSquareMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        copied = original.copy()
        assert copied is not original
        assert copied == original

    def test_getitem_individual_values(self):
        matrix = IntegerSquareMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert matrix[(0, 0)] == matrix[0][0] == 1
        assert matrix[(0, 1)] == matrix[0][1] == 2
        assert matrix[(1, 2)] == matrix[1][2] == 6

    def test_getitem_rows(self):
        matrix = IntegerSquareMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert matrix[0] == [1, 2, 3]
        assert matrix[1] == [4, 5, 6]
        assert matrix[2] == [7, 8, 9]

    def test_setitem_individual_values(self):
        matrix = IntegerSquareMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix[0][0] = 10
        matrix[(1, 1)] = 20
        assert matrix[0][0] == 10
        assert matrix[(1, 1)] == 20

    def test_setitem_rows(self):
        matrix = IntegerSquareMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix[1] = [20, 21, 22]
        assert matrix[1] == [20, 21, 22]
        assert matrix[1][0] == 20
        assert matrix[(1, 2)] == 22

    def test_add(self):
        matrix1 = IntegerSquareMatrix([[1, 2], [3, 4]])
        matrix2 = IntegerSquareMatrix([[5, 6], [7, 8]])

        assert matrix1 + matrix2 == IntegerSquareMatrix([[6, 8], [10, 12]])

    def test_sub(self):
        matrix1 = IntegerSquareMatrix([[1, 2], [3, 4]])
        matrix2 = IntegerSquareMatrix([[5, 6], [7, 8]])

        assert matrix1 - matrix2 == IntegerSquareMatrix([[-4, -4], [-4, -4]])

    def test_neg(self):
        matrix1 = IntegerSquareMatrix([[1, 2], [3, 4]])

        assert -matrix1 == IntegerSquareMatrix([[-1, -2], [-3, -4]])

    def test_mul(self):
        matrix1 = IntegerSquareMatrix([[1, 2], [3, 4]])
        matrix2 = IntegerSquareMatrix([[5, 6], [7, 8]])
        scalar = 2

        assert matrix1 * matrix2 == IntegerSquareMatrix([[19, 22], [43, 50]])
        assert matrix1 * scalar == IntegerSquareMatrix([[2, 4], [6, 8]])

    def test_eq(self):
        matrix1 = IntegerSquareMatrix([[1, 2], [3, 4]])
        matrix2 = IntegerSquareMatrix([[1, 2], [3, 4]])
        matrix3 = IntegerSquareMatrix([[5, 6], [7, 8]])

        assert matrix1 == matrix2
        assert matrix1 != matrix3

    def test_determinant(self):
        matrix1 = IntegerSquareMatrix([[3, 8], [4, 6]])
        assert matrix1.determinant() == -14

        matrix2 = IntegerSquareMatrix([[6, 1, 1], [4, -2, 5], [2, 8, 7]])
        assert matrix2.determinant() == -306

        matrix3 = IntegerSquareMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        assert matrix3.determinant() == 1

        matrix4 = IntegerSquareMatrix([[5]])
        assert matrix4.determinant() == 5


if __name__ == "__main__":
    pytest.main()
