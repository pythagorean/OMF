from matrix.square.integer.scaled.base import FractionScaledMatrix
from number.matric.matrion.core.base import CoreMatrion

from .ops import RadicalFactoredReductionOpsMixin
from ..base import ReductionTransform, DeferTransform


class RadicalFactoredReduction(RadicalFactoredReductionOpsMixin,
                               ReductionTransform):
    is_deterministic = True
    is_reversible = True

    defers_reductions = [DeferTransform.ROOT]

    @classmethod
    def normalize(cls, matrion):
        nonzero_constant_diagonals = cls._find_nonzero_constant_diagonals(
            matrion)

        try:
            first_diagonal = next(nonzero_constant_diagonals)
        except StopIteration:
            return

        first_index, radical = first_diagonal
        if first_index != 1:
            # We are only handling simple scalar roots for now
            return

        if radical != matrion.value.get_scaling() ** -1:
            # This is some multiple of a scalar root
            return

        order = matrion.value.size
        number_diagonals = order * 2 - 1
        number_zero_diagonals = sum(
            1 for _ in cls._find_zero_constant_diagonals(matrion))

        try:
            next_diagonal = next(nonzero_constant_diagonals)
        except StopIteration:
            # This may be a nilpotent or not
            if number_zero_diagonals != number_diagonals - 1:
                return

            matrion.value = FractionScaledMatrix(0)
            return True, order

        next_index, radicand = next_diagonal
        if (number_zero_diagonals != number_diagonals - 2
                or next_index != -(matrion.value.size - 1)):
            # This is not a simple scalar root
            return

        matrion.value = FractionScaledMatrix((radicand, radical))
        return True, order

    @classmethod
    def denormalized(cls, matrion, order):
        return CoreMatrion(matrion.value).root(order).value

    @classmethod
    def annotation(cls, factor):
        return f"root {factor} of"
