from fractions import Fraction
from matrix.square.integer.scaled.base import FractionScaledMatrix
from number.matric.matrion.core.base import CoreMatrion

from .ops import RadicalFactoredReductionOpsMixin
from ..base import ReductionTransform, DeferTransform


class RadicalFactoredReduction(RadicalFactoredReductionOpsMixin,
                               ReductionTransform):
    is_deterministic = True
    is_reversible = True

    defers_reductions = [DeferTransform.ROOT, DeferTransform.MULTIPLY]

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
    def defers_multiply(cls, reduction, other):
        try:
            # We only handle/defer scalars right now
            fractional_other = Fraction(other)
        except TypeError:
            return False
        extra = reduction[2]
        extra['/'] = fractional_other * extra.get('/', 1)
        return True

    @classmethod
    def denormalized(cls, matrion, order, extra=None):
        denormal_value = CoreMatrion(matrion.value).root(order).value
        if extra and (divided := extra.get('/', None)) is not None:
            denormal_value *= Fraction(*divided)
        return denormal_value

    @classmethod
    def annotation(cls, factor, extra=None):
        if extra and (divided := extra.get('/', None)) is not None:
            numer, denom = divided
            if denom == 1:
                return f"{numer} * root {factor} of"
            return f"({Fraction(numer, denom)}) * root {factor} of"
        return f"root {factor} of"

    @classmethod
    def defers(cls, matrion, transform, **kwargs):
        if transform != DeferTransform.MULTIPLY:
            raise ValueError(f"unhandled transform: {transform}")
        performed = matrion.performed_reductions
        for i in range(len(performed)):
            reduction = performed[i]
            transform = reduction[0]
            if cls == transform and cls.defers_multiply(reduction, kwargs['other']):
                return True
        return False
