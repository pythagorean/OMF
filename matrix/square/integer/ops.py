from matrix.square.integer.raw_ops import IntegerMatrixRawOpsMixin
from matrix.square.integer.row_view import IntegerSquareMatrixRowView


class IntegerSquareMatrixOpsMixin(IntegerMatrixRawOpsMixin):
    def _create_row_view(self, index):
        return IntegerSquareMatrixRowView(self, index)

    def __setitem__(self, index, value):
        if isinstance(index, (list, tuple)):
            if not isinstance(value, int):
                raise ValueError("Value to set must be an integer")
        elif not isinstance(value, list) or not all(isinstance(element, int)
                                                    for element in value):
            raise ValueError("Row values must be a list of integers")
        super().__setitem__(index, value)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("Can only add value of the same class")
        if self.size != other.size:
            raise ValueError("Can only add matrix of the same size")
        return self.__class__(self._add_raw(other.matrix))

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("Can only subtract value of the same class")
        if self.size != other.size:
            raise ValueError("Can only subtract matrix of the same size")
        return self.__class__(self._add_raw(other._neg_raw()))

    def __neg__(self):
        return self.__class__(self._neg_raw())

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(self._mul_raw_scalar(other))
        if not isinstance(other, self.__class__):
            raise ValueError(
                "Can only multiply by scalar or value of the same class")
        if self.size != other.size:
            raise ValueError("Can only multiply matrix of the same size")
        return self.__class__(self._mul_raw(other.matrix))

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError("Can only do non-negative integer exponentiation")
        result = self.__class__.identity(self.size)
        base = self.copy()
        while exponent > 0:
            if exponent & 1:
                result *= base
            base *= base
            exponent >>= 1
        return result

    def determinant(self):
        if self.size == 1:
            return self.matrix[0][0]
        if self.size == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        det = 0
        for col_index in range(self.size):
            minor = self._get_raw_minor(0, col_index)
            submatrix = self.__class__(minor)
            det += ((-1) ** col_index) * \
                self.matrix[0][col_index] * submatrix.determinant()
        return det
