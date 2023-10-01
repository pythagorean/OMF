from fractions import Fraction
from math import lcm

from .raw_ops import CoreMatrionRawOpsMixin


class CoreMatrionOpsMixin(CoreMatrionRawOpsMixin):
    def data(self):
        return vars(self)

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

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            try:
                other = Fraction(other)
                return self.__class__(self.value * other)
            except TypeError:
                pass
            try:
                other = self.__class__(other)
            except ValueError:
                raise ValueError(
                    f"Operand {repr(other)} cannot be made {self.__class__.__name__}")
        selfvalue, othervalue = self.value, other.value
        selfsize, othersize = selfvalue.size, othervalue.size
        if selfsize == othersize:
            return self.__class__(selfvalue * othervalue)
        if othersize == 1:
            return self.__class__(selfvalue * othervalue[0, 0])
        if selfsize == 1:
            return self.__class__(othervalue * selfvalue[0, 0])
        lcmsize = lcm(selfsize, othersize)
        selfscaled = self.__class__(
            self._upscale_diagonally_raw(lcmsize // selfsize))
        otherscaled = self.__class__(
            other._upscale_diagonally_raw(lcmsize // othersize))
        return selfscaled * otherscaled
