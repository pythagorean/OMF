from fractions import Fraction

from number.matric.matrion.core.raw_ops import CoreMatrionRawOpsMixin


class CoreMatrionOpsMixin(CoreMatrionRawOpsMixin):
    def copy(self, **kwargs):
        return self.__class__(self, **kwargs)

    def __pow__(self, exponent):
        if isinstance(exponent, int):
            exponent = Fraction(exponent)
        elif isinstance(exponent, tuple) and len(exponent) == 2:
            exponent = Fraction(*exponent)
        if not isinstance(exponent, Fraction):
            raise ValueError("Exponent must be an integer, tuple or fraction")
        if exponent.denominator == 1:
            return self.__class__(self.value ** exponent.numerator)
        root = self.root(exponent.denominator)
        if exponent.numerator == 1:
            return root
        return self.__class__(root.value ** exponent.numerator)

    def root(self, order):
        if not isinstance(order, int) or order <= 0:
            raise ValueError("The root order must be a positive integer.")
        if order == 1:
            return self
        self_size = self.value.size
        root_matrix = self._nilpotent(order)._upscale_diagonally_raw(self_size)
        root_size = len(root_matrix)
        row_offset = root_size - self_size
        for row in range(self_size):
            for col in range(self_size):
                root_matrix[row + row_offset][col] = self.value[row, col]
        return self.__class__(root_matrix)

    @classmethod
    def _nilpotent(cls, order):
        matrix = [
            [1 if col == row + 1 else 0
             for col in range(order)]
            for row in range(order)]
        return cls(matrix)
