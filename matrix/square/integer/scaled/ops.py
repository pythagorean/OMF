from math import gcd, lcm
from fractions import Fraction
from matrix.square.integer.base import IntegerSquareMatrix
from matrix.square.integer.scaled.row_view import FractionScaledMatrixRowView


class FractionScaledMatrixOpsMixin:
    @classmethod
    def identity(cls, size):
        matrix = cls._identity_raw(size)
        instance = cls(elements=matrix, normalize=False)
        instance.reduced = True
        return instance

    def copy(self):
        new_matrix = self.__class__(self._copy_raw(), normalize=False)
        new_matrix.scaling = self.scaling
        new_matrix.reduced = self.reduced
        return new_matrix

    def _create_row_view(self, index):
        return FractionScaledMatrixRowView(self, index)

    def __getitem__(self, index):
        if isinstance(index, int):
            # calls self._create_row_view(index)
            return super().__getitem__(index)
        scaling = self.get_scaling()
        return super().__getitem__(index) * scaling

    def __setitem__(self, index, value):
        size = self.size
        adjustment_matrix = [[0 for _ in range(size)] for _ in range(size)]
        if isinstance(index, tuple):
            scaling = self._setitem_handle_tuple_index(
                adjustment_matrix, index, value)
        elif isinstance(index, int):
            if not isinstance(value, list) or len(value) != size:
                raise ValueError(f"Value must be a row of size {size}")
            scaling = self._setitem_handle_integer_index(
                adjustment_matrix, index, value)
        else:
            raise ValueError("Unsupported index type")
        adjustment = self.__class__(adjustment_matrix, scaling=scaling)
        adjusted = self + adjustment
        self.matrix, self.scaling, self.reduced = (
            adjusted.matrix, adjusted.scaling, adjusted.reduced)

    def _setitem_handle_tuple_index(self, adjustment_matrix, index, value):
        row, col = index
        adjustment_matrix[row][col] = 1
        self.matrix[row][col] = 0
        return Fraction(value).as_integer_ratio()

    def _setitem_handle_integer_index(self, adjustment_matrix, index, value):
        row = index
        if all(isinstance(val, int) for val in value):
            adjustment_matrix[row] = value
            return (1, 1)
        value = [Fraction(val) for val in value]
        denominators = [val.denominator for val in value]
        common_denominator = self._lcm_nonzero_elements(*denominators)
        scaled_row = [val.numerator * common_denominator //
                      val.denominator for val in value]
        adjustment_matrix[row] = scaled_row
        self.matrix[row] = [0 for _ in range(self.size)]
        return (1, common_denominator)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                "Can only compare another instance of the same class.")
        return self.scaling == other.scaling and super().__eq__(other)

    def equivalent(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                "Can only compare another instance of the same class.")
        return self.normalized() == other.normalized()

    def normalized(self):
        if self.reduced:
            return self
        self_copy = self.copy()
        self_copy._normalize()
        return self_copy

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Can only add another instance of the same class.")
        self_scaled, other_scaled = self.get_scaling(), other.get_scaling()
        if self_scaled != other_scaled:
            return self._add_other_scaling(other, self_scaled, other_scaled)
        added = super().__add__(other)
        new_scaling = self_scaled * added.get_scaling()
        return self.__class__(added.matrix, scaling=new_scaling)

    def _add_other_scaling(self, other, self_scaled, other_scaled):
        if self.size != other.size:
            raise ValueError("Can only add matrices of the same size.")
        if self_scaled.denominator != other_scaled.denominator:
            return self._add_other_denominator(other, self_scaled, other_scaled)
        self_multiplier, other_multiplier = self_scaled.numerator, other_scaled.numerator
        super_self = IntegerSquareMatrix(self.matrix) * self_multiplier
        super_other = IntegerSquareMatrix(other.matrix) * other_multiplier
        added = super_self + super_other
        new_scaling = (1, self_scaled.denominator)
        return self.__class__(added.matrix, scaling=new_scaling)

    def _add_other_denominator(self, other, self_scaled, other_scaled):
        lcm_denominator = lcm(
            self_scaled.denominator, other_scaled.denominator)
        self_multiplier = self_scaled.numerator * (lcm_denominator //
                                                   self_scaled.denominator)
        other_multiplier = other_scaled.numerator * (lcm_denominator //
                                                     other_scaled.denominator)
        super_self = IntegerSquareMatrix(self.matrix) * self_multiplier
        super_other = IntegerSquareMatrix(other.matrix) * other_multiplier
        added = super_self + super_other
        new_scaling = (1, lcm_denominator)
        return self.__class__(added.matrix, scaling=new_scaling)

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        return self * (-1)

    def __mul__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            other = Fraction(*other)
        elif isinstance(other, int):
            other = Fraction(other)
        if isinstance(other, Fraction):
            scalar = other
            mul_result = self.copy()
        elif isinstance(other, self.__class__):
            scalar = self.get_scaling() * other.get_scaling()
            mul_result = super().__mul__(other)
        else:
            raise ValueError("Unsupported multiplication type")
        mul_scaling = mul_result.get_scaling() * scalar
        mul_matrix = mul_result.matrix
        return self.__class__(mul_matrix, scaling=mul_scaling)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        elif isinstance(other, tuple) and len(other) == 2:
            other = Fraction(*other)
        if isinstance(other, Fraction):
            return self * (1 / other)
        elif isinstance(other, self.__class__):
            return self * other.inverse()
        else:
            raise ValueError("Unsupported division")

    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            raise ValueError("Exponent must be an integer")
        if exponent < 0:
            return self.inverse().__pow__(-exponent)
        return super().__pow__(exponent) * self.get_scaling() ** exponent

    def determinant(self):
        scaling = self.get_scaling() ** self.size
        return scaling * super().determinant()

    def inverse(self):
        determinant = self.determinant()
        if (determinant == 0):
            raise ValueError("Matrix has no inverse")
        return self.adjoint() / determinant

    def transpose(self):
        transpose_matrix = self._transpose_raw()
        return self.__class__(transpose_matrix, scaling=self.scaling)

    def adjoint(self):
        if self.size == 1:
            return self
        cofactor_matrix = []
        for i in range(self.size):
            cofactor_row = []
            for j in range(self.size):
                minor = self._get_raw_minor(i, j)
                submatrix = self.__class__(minor, scaling=self.scaling)
                cofactor = ((-1) ** (i + j)) * submatrix.determinant()
                cofactor_row.append(cofactor)
            cofactor_matrix.append(cofactor_row)
        cofactors = self.__class__(cofactor_matrix)
        return cofactors.transpose()
