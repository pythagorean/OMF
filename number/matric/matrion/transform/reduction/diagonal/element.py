from number.matric.matrion.transform.reduction.base import ReductionTransform

from matrix.square.integer.base import IntegerSquareMatrix
from matrix.square.integer.scaled.base import FractionScaledMatrix


class ElementDiagonalReduction(ReductionTransform):
    is_deterministic = True
    is_reversible = True

    @classmethod
    def normalize(cls, matrion):
        if matrion.value[0, -1] or matrion.value[-1, 0]:
            return
        unreduced_size = matrion.value.size
        for try_scaled in range(matrion.value.size >> 1, 1, -1):
            if matrion.value.size % try_scaled:
                continue
            scales = []
            stopped = False
            for start_row in range(0, matrion.value.size, try_scaled):
                for start_col in range(0, matrion.value.size, try_scaled):
                    end_row = start_row + try_scaled - 1
                    end_col = start_col + try_scaled - 1
                    value = FractionScaledMatrix(matrion._extract_submatrix_raw(
                        start_row, end_row, start_col, end_col))
                    bin, mul = IntegerSquareMatrix(
                        value.matrix).is_zeros_or_identity()
                    if not bin:
                        stopped = True
                        break
                    scales.append(value.get_scaling() * mul)
                if stopped:
                    break
            if not stopped:
                matrion.value = FractionScaledMatrix(
                    scales, scaling=matrion.value.scaling)
                return True, unreduced_size // matrion.value.size

    @classmethod
    def denormalized(cls, matrion, factor):
        return FractionScaledMatrix(matrion._upscale_diagonally_raw(scale=factor))
