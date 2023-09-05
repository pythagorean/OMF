from matrix.square.integer.scaled.base import FractionScaledMatrix
from number.matric.matrion.core.base import CoreMatrion

from number.matric.matrion.methods.reduction.base import ReductionMethod, DeferMethod

from number.matric.matrion.methods.reduction.radical.ops import RadicalFactoredReductionOpsMixin


class RadicalFactoredReduction(RadicalFactoredReductionOpsMixin,
                               ReductionMethod):
    is_deterministic = True
    is_reversible = True
    defers_methods = [DeferMethod.ROOT]

    @classmethod
    def normalize(cls, matrion):
        nonzero_constant_diagonals = cls._find_nonzero_constant_diagonals(
            matrion)

        try:
            first_diagonal = next(nonzero_constant_diagonals)
        except StopIteration:
            return

        first_index, radical = first_diagonal
        if first_index != 1 or radical != 1:
            # We are only handling simple integer non-scalar multiplied roots for now
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
            # This is not a simple integer root
            return

        matrion.value = FractionScaledMatrix(
            radicand, scaling=matrion.value.scaling)
        return True, order

    @classmethod
    def denormalized(cls, matrion, order):
        return CoreMatrion(matrion).root(order).value

    @classmethod
    def annotation(cls, factor):
        return f"root {factor} of"
