from number.matric.matrion.transform.reduction.base import ReductionTransform

from matrix.square.integer.base import IntegerSquareMatrix
from matrix.square.integer.scaled.base import FractionScaledMatrix


class BlockDiagonalReduction(ReductionTransform):
    is_deterministic = True
    is_reversible = True

    @classmethod
    def normalize(cls, matrion):
        unreduced_size = matrion.value.size
        diagonals = matrion._diagonal_submatrices_raw()
        if len(diagonals) > 1:
            first_diagonal_submatrix = IntegerSquareMatrix(diagonals[0])
            if all(IntegerSquareMatrix(submatrix) == first_diagonal_submatrix
                   for submatrix in diagonals[1:]):
                matrion.value = FractionScaledMatrix(
                    first_diagonal_submatrix.matrix, scaling=matrion.value.scaling)
                if matrion.value.size == 1:
                    return True, unreduced_size
        if matrion.value.size < unreduced_size:
            return True, unreduced_size // matrion.value.size

    @classmethod
    def denormalized(cls, matrion, factor):
        return FractionScaledMatrix(matrion._upscale_diagonally_raw(scale=factor, block=True))
