import pytest
from fractions import Fraction
from matrix.square.integer.scaled.base import *


class TestFractionScaledMatrix:
    def test_initialization_with_scaling(self):
        matrix_1 = FractionScaledMatrix([1, 2, 3, 4], scaling=(2, 3))
        matrix_2 = FractionScaledMatrix([1, 2, 3, 4]) * 2 / 3
        assert matrix_1.matrix == [[1, 2], [3, 4]]
        assert matrix_1.scaling == (2, 3)
        assert matrix_1 == matrix_2

    def test_negative_value(self):
        matrix_1 = FractionScaledMatrix(-8)
        matrix_2 = FractionScaledMatrix([-8, -8, -8, -8])
        assert matrix_1.matrix == [[1]]
        assert matrix_1.scaling == (-8, 1)
        assert matrix_2.matrix == [[1, 1], [1, 1]]
        assert matrix_2.scaling == (-8, 1)

    def test_invalid_scaling(self):
        with pytest.raises(ValueError):
            FractionScaledMatrix([1, 2, 3, 4], scaling=(2, 0))

    def test_invalid_element_count(self):
        with pytest.raises(ValueError):
            FractionScaledMatrix([1, 2, 3])

    def test_representation(self):
        assert repr(FractionScaledMatrix(Fraction(1, 2))
                    ) == "FractionScaledMatrix([[1]], scaling=(1, 2))"
        assert repr(FractionScaledMatrix((1, 2))
                    ) == "FractionScaledMatrix([[1]], scaling=(1, 2))"
        assert repr(FractionScaledMatrix(1)
                    ) == "FractionScaledMatrix([[1]])"
        assert repr(FractionScaledMatrix(1) / 2
                    ) == "FractionScaledMatrix([[1]], scaling=(1, 2))"

    def test_invalid_fractional_input(self):
        with pytest.raises(ValueError):
            FractionScaledMatrix(1 / 2)
        with pytest.raises(TypeError):
            FractionScaledMatrix(1, 2)

    def test_initialize_from_fraction_list(self):
        # Using Fraction objects
        matrix_1 = FractionScaledMatrix(
            [Fraction(1, 2), Fraction(3, 2), Fraction(5, 2), Fraction(7, 2)])
        assert matrix_1.matrix == [[1, 3], [5, 7]]
        assert matrix_1.scaling == (1, 2)

        # Using tuples
        matrix_2 = FractionScaledMatrix([(1, 2), (3, 2), (5, 2), (7, 2)])
        assert matrix_2.matrix == [[1, 3], [5, 7]]
        assert matrix_2.scaling == (1, 2)

        # Using mixed tuples and fractions
        matrix_3 = FractionScaledMatrix(
            [Fraction(1, 2), (3, 2), Fraction(5, 2), (7, 2)])
        assert matrix_3.matrix == [[1, 3], [5, 7]]
        assert matrix_3.scaling == (1, 2)

        # Custom scaling factor
        matrix_4 = FractionScaledMatrix([Fraction(1, 2), Fraction(
            3, 2), Fraction(5, 2), Fraction(7, 2)], scaling=(3, 4))
        assert matrix_4.matrix == [[1, 3], [5, 7]]
        assert matrix_4.scaling == (3, 8)

        # Custom scaling factor as tuple
        matrix_5 = FractionScaledMatrix([Fraction(1, 2), Fraction(
            3, 2), Fraction(5, 2), Fraction(7, 2)], scaling=(3, 4))
        assert matrix_5.matrix == [[1, 3], [5, 7]]
        assert matrix_5.scaling == (3, 8)

    def test_identity(self):
        size = 3
        matrix = FractionScaledMatrix.identity(size)
        expected = FractionScaledMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        assert matrix == expected

    def test_copy(self):
        original = FractionScaledMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        copied = original.copy()
        assert copied is not original
        assert copied == original

    def test_getitem(self):
        # Test with single integer
        matrix = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(1, 2))
        row_view = matrix[0]
        assert row_view[0] == Fraction(1, 2)
        assert row_view[1] == Fraction(2, 2)

        # Test with tuple
        value = matrix[0, 1]
        assert value == matrix[(0, 1)]
        assert value == Fraction(2, 2)

    def test_setitem(self):
        # Test with single integer
        matrix = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(1, 2))
        matrix[0] = [Fraction(3, 2), Fraction(4, 2)]
        assert matrix[0, 0] == Fraction(3, 2)
        assert matrix[(0, 1)] == Fraction(4, 2)

        # Test with tuple
        matrix = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(1, 2))
        matrix[(0, 1)] = Fraction(5, 2)
        matrix[1, 1] = Fraction(7, 2)
        assert matrix[0, 1] == Fraction(5, 2)
        assert matrix[(1, 1)] == Fraction(7, 2)

    def test_add(self):
        matrix1 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(2, 3))
        matrix2 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(2, 3))
        assert matrix1 + \
            matrix2 == FractionScaledMatrix([[3, 4], [5, 6]], scaling=(4, 3))

        # Test with different scaling factors
        matrix3 = FractionScaledMatrix([[1, 2], [3, 4]])
        matrix4 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(1, 2))
        assert matrix3 + \
            matrix4 == FractionScaledMatrix(
                [[7, 10], [13, 16]], scaling=(1, 2))

        # Test with negative scaling factors
        matrix5 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(-1, 2))
        matrix6 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(2, 1))
        assert matrix5 + \
            matrix6 == FractionScaledMatrix(
                [[19, 22], [25, 28]], scaling=(1, 2))

        # Zero scaling factor on one matrix
        matrix1 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(0, 1))
        matrix2 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(1, 2))
        assert matrix1 + \
            matrix2 == FractionScaledMatrix([[5, 6], [7, 8]], scaling=(1, 2))

        # Zero scaling factor on both matrices
        matrix3 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(0, 1))
        matrix4 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(0, 1))
        assert matrix3 + \
            matrix4 == FractionScaledMatrix([[0, 0], [0, 0]], scaling=(1, 1))

    def test_sub(self):
        # Test with same scaling factors
        matrix1 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(2, 3))
        matrix2 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(2, 3))
        assert matrix1 - \
            matrix2 == FractionScaledMatrix([[1, 1], [1, 1]], scaling=(-8, 3))

        # Test with different scaling factors
        matrix3 = FractionScaledMatrix([[1, 2], [3, 4]])
        matrix4 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(1, 2))
        assert matrix3 - \
            matrix4 == FractionScaledMatrix([[3, 2], [1, 0]], scaling=(-1, 2))

        # Test with negative scaling factors
        matrix5 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(-1, 2))
        matrix6 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(2, 1))
        assert matrix5 - \
            matrix6 == FractionScaledMatrix(
                [[21, 26], [31, 36]], scaling=(-1, 2))

        # Test with zero scaling factor
        matrix7 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(0, 1))
        matrix8 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(1, 2))
        assert matrix7 - \
            matrix8 == FractionScaledMatrix([[5, 6], [7, 8]], scaling=(-1, 2))

    def test_neg(self):
        matrix1 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(2, 3))
        matrix2 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(-2, 3))
        assert -matrix1 == matrix2
        assert -matrix2 == matrix1

    def test_mul(self):
        matrix1 = FractionScaledMatrix([[1, 2], [3, 4]])
        matrix2 = FractionScaledMatrix([[5, 6], [7, 8]])
        scalar = 2
        fraction_scalar = Fraction(2, 3)

        assert matrix1 * matrix2 == FractionScaledMatrix([[19, 22], [43, 50]])
        assert matrix1 * \
            scalar == FractionScaledMatrix([[1, 2], [3, 4]], scaling=(2, 1))
        assert matrix1 * \
            (2, 3) == FractionScaledMatrix([[1, 2], [3, 4]], scaling=(2, 3))
        assert matrix1 * \
            fraction_scalar == FractionScaledMatrix(
                [[1, 2], [3, 4]], scaling=(2, 3))

        # Test with different scaling factors
        matrix3 = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(2, 3))
        matrix4 = FractionScaledMatrix([[5, 6], [7, 8]], scaling=(3, 4))
        assert matrix3 * \
            matrix4 == FractionScaledMatrix(
                [[19, 22], [43, 50]], scaling=(1, 2))

    def test_determinant(self):
        matrix1 = FractionScaledMatrix([[3, 8], [4, 6]])
        assert matrix1.determinant() == -14

        matrix2 = FractionScaledMatrix([[6, 1, 1], [4, -2, 5], [2, 8, 7]])
        assert matrix2.determinant() == -306

        matrix3 = FractionScaledMatrix(
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) * 2/3
        assert matrix3.determinant() == Fraction(8, 27)

        matrix4 = FractionScaledMatrix([[5]])
        assert matrix4.determinant() == 5

    def test_inverse(self):
        # Test with identity matrix
        matrix = FractionScaledMatrix.identity(3)
        assert matrix.inverse() == matrix

        # Test with known inverse
        matrix = FractionScaledMatrix([[1, 2], [3, 4]])
        expected_inverse = FractionScaledMatrix(
            [[-4, 2], [3, -1]], scaling=(1, 2))
        assert matrix.inverse() == expected_inverse

        # Test with non-invertible matrix
        matrix = FractionScaledMatrix([[1, 2], [1, 2]], scaling=(1, 1))
        with pytest.raises(ValueError):
            matrix.inverse()

        # Test with scaling
        matrix = FractionScaledMatrix([[1, 2], [3, 4]], scaling=(2, 1))
        expected_inverse = FractionScaledMatrix(
            [[-4, 2], [3, -1]], scaling=(1, 4))
        assert matrix.inverse() == expected_inverse

    def test_power(self):
        matrix = FractionScaledMatrix([[1, 2], [3, 4]])
        power = 2
        expected_power = FractionScaledMatrix([[7, 10], [15, 22]])
        assert matrix ** power == expected_power

    def test_transpose(self):
        matrix = FractionScaledMatrix([[1, 2], [3, 4]])
        expected_transpose = FractionScaledMatrix([[1, 3], [2, 4]])
        assert matrix.transpose() == expected_transpose

    def test_division(self):
        matrix_a = FractionScaledMatrix([[1, 2], [3, 4]])
        matrix_b = FractionScaledMatrix([[9, 8], [6, 5]])
        expected_division = FractionScaledMatrix(
            [[7, -10], [9, -12]], scaling=(1, 3))
        assert matrix_a / matrix_b == expected_division


if __name__ == "__main__":
    pytest.main()
