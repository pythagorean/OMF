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

    def non_zero_indices(self):
        matrix = self.matrix
        rows, cols = len(matrix), len(matrix[0])
        non_zero_coords = []
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] != 0:
                    non_zero_coords.append((i, j))
        return non_zero_coords
