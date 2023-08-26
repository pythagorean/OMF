from matrix.square.raw_ops import SquareMatrixRawOpsMixin
from matrix.square.row_view import SquareMatrixRowView


class SquareMatrixOpsMixin(SquareMatrixRawOpsMixin):
    @classmethod
    def identity(cls, size):
        matrix = cls._identity_raw(size)
        return cls(matrix)

    def _create_row_view(self, index):
        return SquareMatrixRowView(self, index)

    def __setitem__(self, index, value):
        if isinstance(index, (list, tuple)) and len(index) == 2:
            row, col = index
            self.matrix[row][col] = value
            return
        if not isinstance(value, list):
            raise ValueError("Row values to set must be a list")
        if len(value) != self.size:
            raise ValueError(f"Row must have {self.size} elements")
        self.matrix[index] = value

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.size == other.size:
            return all(a == b for a, b in zip(self.matrix, other.matrix))
        return False
