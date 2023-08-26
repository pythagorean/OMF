from matrix.square.integer.base import IntegerSquareMatrix


class FractionScaledMatrixNormMixin:
    def _normalize(self):
        if self.reduced:
            return
        scaled = self.get_scaling()
        if not scaled.numerator:
            self.matrix = [[0 for _ in row] for row in self.matrix]
            self.scaling = (1, 1)
            self.reduced = True
            return
        elements = self.matrix_as_flat_list()
        if any(element < 0 for element in elements):
            if scaled < 0 or all(element <= 0 for element in elements):
                super_self = IntegerSquareMatrix(self.matrix) * (-1)
                self.matrix = super_self.matrix
                scaled *= -1
        element_gcd = self._gcd_nonzero_elements(*elements)
        if element_gcd > 1:
            self.matrix = [[element // element_gcd for element in row]
                           for row in self.matrix]
        scaled *= element_gcd
        self.scaling = scaled.as_integer_ratio()
        self.reduced = True
