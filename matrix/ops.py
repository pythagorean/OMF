from matrix.raw_ops import MatrixRawOpsMixin
from matrix.row_view import MatrixRowView


class MatrixOpsMixin(MatrixRawOpsMixin):
    def copy(self):
        return self.__class__(self._copy_raw())

    def transpose(self):
        return self.__class__(self._transpose_raw())

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._create_row_view(index)
        elif not (isinstance(index, (list, tuple)) and len(index) == 2):
            raise TypeError("Unsupported index type or number of coordinates")
        row, col = index
        return self.matrix[row][col]

    def _create_row_view(self, index):
        return MatrixRowView(self, index)
