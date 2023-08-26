class MatrixRawOpsMixin:
    def _copy_raw(self):
        return [row[:] for row in self.matrix]

    def _transpose_raw(self):
        return list(map(list, zip(*self.matrix)))

    def _add_raw(self, other_matrix):
        return [[a + b for a, b in zip(row_self, row_other)]
                for row_self, row_other in zip(self.matrix, other_matrix)]

    def _neg_raw(self):
        return [[-element for element in row] for row in self.matrix]
