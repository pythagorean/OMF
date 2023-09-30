from fractions import Fraction
from matrix.square.integer.scaled.base import FractionScaledMatrix
from number.matric.matrion.core.base import CoreMatrion


class RadicalFactoredReductionNormMixin:
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
            # We are only handling scalar roots for now
            return

        extra = {}
        scaling = matrion.value.get_scaling()
        if radical != scaling ** -1:
            # This may be a scalar multiple of a scalar root
            matrion.value.set_scaling((1, radical))
            extra['/'] = (radical * scaling).as_integer_ratio()

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
            return True, order, extra

        next_index, radicand = next_diagonal
        if (number_zero_diagonals != number_diagonals - 2
                or next_index != -(matrion.value.size - 1)):
            # This is not a single scalar root
            return

        matrion.value = FractionScaledMatrix((radicand, radical))
        return True, order, extra

    @classmethod
    def denormalized(cls, matrion, order, extra=None):
        denormal_value = CoreMatrion(matrion.value).root(order).value
        if extra and (divided := extra.get('/', None)) is not None:
            denormal_value *= Fraction(*divided)
        return denormal_value
