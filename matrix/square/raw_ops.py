class SquareMatrixRawOpsMixin:
    @classmethod
    def _identity_raw(cls, size):
        matrix = [[1 if i == j else 0 for j in range(
            size)] for i in range(size)]
        return matrix

    def _mul_raw(self, other_matrix):
        return [[sum(a * b for a, b in zip(row_a, col_b))
                 for col_b in zip(*other_matrix)] for row_a in self.matrix]
