from fractions import Fraction

from ..base import DeferTransform


class RadicalFactoredReductionOpsMixin:
    @classmethod
    def _find_nonzero_constant_diagonals(cls, matrion):
        """Yields:
            Tuples (diagonal index, constant value) across the columns then the rows
        """
        matrix_size = matrion.value.size
        matrix_data = matrion.value.matrix
        for idx in range(matrix_size):
            if (constant_value := matrix_data[0][idx]) == 0:
                continue
            if idx == matrix_size - 1 or all(constant_value == matrix_data[i][idx + i]
                                             for i in range(1, matrix_size - idx)):
                yield idx, constant_value

        for idx in range(1, matrix_size):
            if (constant_value := matrix_data[idx][0]) == 0:
                continue
            if idx == matrix_size - 1 or all(constant_value == matrix_data[idx + i][i]
                                             for i in range(1, matrix_size - idx)):
                yield -idx, constant_value

    @classmethod
    def _find_zero_constant_diagonals(cls, matrion):
        """Yields:
            Diagonal index across the columns then the rows
        """
        matrix_size = matrion.value.size
        matrix_data = matrion.value.matrix
        for idx in range(matrix_size):
            if matrix_data[0][idx] != 0:
                continue
            if idx == matrix_size - 1 or all(matrix_data[i][idx + i] == 0
                                             for i in range(matrix_size - idx)):
                yield idx

        for idx in range(1, matrix_size):
            if matrix_data[idx][0] != 0:
                continue
            if idx == matrix_size - 1 or all(matrix_data[idx + i][i] == 0
                                             for i in range(matrix_size - idx)):
                yield -idx

    @classmethod
    def defers_multiply(cls, reduction, other):
        try:
            # We only handle/defer scalars right now
            other = Fraction(other)
        except TypeError:
            return False
        extra = reduction[2]
        extra['/'] = (other * extra.get('/', 1)).as_integer_ratio()
        return True

    @classmethod
    def annotation(cls, factor, extra=None):
        if extra and (divided := extra.get('/', None)) is not None:
            numer, denom = divided
            if denom == 1:
                return f"({numer} * root {factor}) of"
            return f"(({Fraction(numer, denom)}) * root {factor}) of"
        return f"root {factor} of"

    @classmethod
    def defers(cls, matrion, transform, **kwargs):
        if transform != DeferTransform.MULTIPLY:
            raise ValueError(f"unhandled transform: {transform}")
        performed = matrion.performed_reductions
        for reduction in reversed(performed):
            transform = reduction[0]
            if cls == transform and cls.defers_multiply(reduction, kwargs['other']):
                return True
        return False
