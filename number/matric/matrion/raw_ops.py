class MatrionRawOpsMixin:
    def _zeros_raw(self, size, set_fractional=False):
        return self.value._zeros_raw(size, set_fractional)

    def _identity_raw(self, size):
        return self.value._identity_raw(size)

    def _upscale_diagonally_raw(self, scale, *, block=False):
        """
        If block=False, each element of the original matrix is replicated 'scale' times diagonally.
        If block=True, the original matrix itself is replicated as a block 'scale' times diagonally.
        """
        self_size = self.value.size
        new_size = self_size * scale
        matrix = self._zeros_raw(new_size, set_fractional=True)
        for i in range(self_size):
            for j in range(self_size):
                if (value := self.value[i, j]) != 0:
                    if not block:
                        for diag in range(scale):
                            matrix[i*scale + diag][j*scale + diag] = value
                    else:
                        for diag in range(scale):
                            offset = diag * self_size
                            matrix[i + offset][j + offset] = value
        return matrix

    def _extract_submatrix_raw(self, start_row, end_row, start_col, end_col):
        return [row[start_col:end_col + 1] for row in
                self.value.matrix[start_row:end_row + 1]]

    def _diagonal_submatrices_raw(self):
        submatrices = []
        size = self.value.size

        def is_all_zeros(submatrix):
            return all(cell == 0 for row in submatrix for cell in row)

        diagonal_offset, row_col_start, row_col_end = 0, 0, size - 1
        while True:
            diagonal_offset += 1
            row_col_next = row_col_start + diagonal_offset
            row_col_boundary = row_col_next - 1
            right_submatrix = self._extract_submatrix_raw(
                row_col_start, row_col_boundary, row_col_next, row_col_end)
            if not is_all_zeros(right_submatrix):
                continue
            lower_submatrix = self._extract_submatrix_raw(
                row_col_next, row_col_end, row_col_start, row_col_boundary)
            if not is_all_zeros(lower_submatrix):
                continue
            submatrices.append(self._extract_submatrix_raw(
                row_col_start, row_col_boundary, row_col_start, row_col_boundary))
            if row_col_boundary >= row_col_end:
                return submatrices
            diagonal_offset, row_col_start = 0, row_col_next
