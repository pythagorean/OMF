class IntegerMatrixRawOpsMixin:
    def _mul_raw_scalar(self, other_scalar):
        return [[element * other_scalar for element in row] for row in self.matrix]

    def _get_raw_minor(self, row, col):
        return [r[:col] + r[col+1:] for r in (self.matrix[:row] + self.matrix[row+1:])]
