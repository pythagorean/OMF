import pytest
from sympy import Matrix

from matrix.square.integer.base import IntegerSquareMatrix
from matrix.square.integer.scaled.base import FractionScaledMatrix
from number.matric.matrion.base import Matrion


class TestMatrion:
    @pytest.mark.parametrize("size", [2, 3, 4])
    def test_identity_normalization(self, size):
        matrix = IntegerSquareMatrix.identity(size)
        matrion = Matrion(matrix.matrix)
        expected = FractionScaledMatrix([[1]])
        assert matrion.value == expected

    @pytest.mark.parametrize("size", [2, 3, 4])
    def test_zeros_normalization(self, size):
        matrix = IntegerSquareMatrix.zeros(size)
        matrion = Matrion(matrix.matrix)
        expected = FractionScaledMatrix([[0]])
        assert matrion.value == expected

    @pytest.mark.parametrize("scalar", [1, 2, 3, 0, -1])
    def test_scalar_normalization(self, scalar):
        matrion = Matrion(scalar)
        expected = FractionScaledMatrix([[scalar]])
        assert matrion.value == expected

    @pytest.mark.parametrize("scalar", [1, 2, 3, 0, -1])
    def test_scaled_identity_normalization(self, scalar):
        size = 3
        matrix = IntegerSquareMatrix.identity(size) * scalar
        matrion = Matrion(matrix.matrix)
        expected = FractionScaledMatrix([[scalar]])
        assert matrion.value == expected

    # The block diagonal matrix that represents sqrt(2) redundantly.
    @pytest.mark.parametrize("matrix_data, expected", [
        ([[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]], [[0, 1], [2, 0]]),
        # A block diagonal matrix with repeating identity blocks scaled by 1 and 2.
        ([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]],
            [[1, 0], [0, 2]])
    ])
    def test_block_diagonal_normalization(self, matrix_data, expected):
        matrion = Matrion(matrix_data)
        expected = FractionScaledMatrix(expected)
        assert matrion.value == expected

    def compare_get_diag_with_sympy(self, matrix_data):
        our_matrix = Matrion(matrix_data, normalize=False)
        sympy_matrix = Matrix(matrix_data)
        custom_blocks = our_matrix._diagonal_submatrices_raw()
        sympy_blocks = sympy_matrix.get_diag_blocks()
        # Convert sympy's Matrix objects to regular lists for easy comparison
        sympy_blocks = [block.tolist() for block in sympy_blocks]
        assert custom_blocks == sympy_blocks

    def test_get_diag(self):
        # single element
        self.compare_get_diag_with_sympy([[1]])
        # diagonal
        self.compare_get_diag_with_sympy([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
        # full matrix
        self.compare_get_diag_with_sympy([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        # zero matrix
        self.compare_get_diag_with_sympy([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        # mixed blocks
        self.compare_get_diag_with_sympy(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 3, 0], [0, 0, 0, 3]])


if __name__ == "__main__":
    pytest.main()
