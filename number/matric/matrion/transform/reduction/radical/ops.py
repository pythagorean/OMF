class RadicalFactoredReductionOpsMixin:
    @classmethod
    def _find_nonzero_constant_diagonals(cls, matrion):
        """Yields:
            Tuples (diagonal index, constant value) across the columns then the rows
        """
        matrix_size = matrion.value.size
        matrix_data = matrion.value.matrix
        for idx in range(matrix_size):
            if (constant_value := matrix_data[0][idx]) == 0:
                continue
            if idx == matrix_size - 1 or all(constant_value == matrix_data[i][idx + i]
                                             for i in range(1, matrix_size - idx)):
                yield idx, constant_value

        for idx in range(1, matrix_size):
            if (constant_value := matrix_data[idx][0]) == 0:
                continue
            if idx == matrix_size - 1 or all(constant_value == matrix_data[idx + i][i]
                                             for i in range(1, matrix_size - idx)):
                yield -idx, constant_value

    @classmethod
    def _find_zero_constant_diagonals(cls, matrion):
        """Yields:
            Diagonal index across the columns then the rows
        """
        matrix_size = matrion.value.size
        matrix_data = matrion.value.matrix
        for idx in range(matrix_size):
            if matrix_data[0][idx] != 0:
                continue
            if idx == matrix_size - 1 or all(matrix_data[i][idx + i] == 0
                                             for i in range(matrix_size - idx)):
                yield idx

        for idx in range(1, matrix_size):
            if matrix_data[idx][0] != 0:
                continue
            if idx == matrix_size - 1 or all(matrix_data[idx + i][i] == 0
                                             for i in range(matrix_size - idx)):
                yield -idx
