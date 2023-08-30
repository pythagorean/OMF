from matrix.square.integer.base import IntegerSquareMatrix
from matrix.square.integer.scaled.base import FractionScaledMatrix


class MatrionNormMixin:
    def _block_reduced_notif(self, scale):
        """
        Notification method for block diagonal reduction. 
        Intended to be overridden by subclasses.
        """
        pass

    def _element_reduced_notif(self, scale):
        """
        Notification method for element diagonal reduction. 
        Intended to be overridden by subclasses.
        """
        pass

    def _normalize(self):
        if self.reduced:
            return
        self.reduced = True
        if self.value.size == 1:
            return
        unreduced_size = self.value.size
        diagonals = self._diagonal_submatrices_raw()
        if len(diagonals) > 1:
            first_diagonal = IntegerSquareMatrix(diagonals[0])
            if all(IntegerSquareMatrix(diagonal) == first_diagonal for diagonal in diagonals[1:]):
                self.value = FractionScaledMatrix(
                    first_diagonal.matrix, scaling=self.value.scaling)
                if self.value.size == 1:
                    self._block_reduced_notif(unreduced_size)
                    return
        if self.value.size < unreduced_size:
            self._block_reduced_notif(unreduced_size // self.value.size)
        if self.value[0, -1] or self.value[-1, 0]:
            return
        unreduced_size = self.value.size
        for try_scaled in range(self.value.size >> 1, 1, -1):
            if self.value.size % try_scaled:
                continue
            scales = []
            stopped = False
            for start_row in range(0, self.value.size, try_scaled):
                for start_col in range(0, self.value.size, try_scaled):
                    end_row = start_row + try_scaled - 1
                    end_col = start_col + try_scaled - 1
                    value = FractionScaledMatrix(self._extract_submatrix_raw(
                        start_row, end_row, start_col, end_col))
                    bin, mul = IntegerSquareMatrix(
                        value.matrix).is_zeros_or_identity()
                    if not bin:
                        stopped = True
                        break
                    scales.append(value.get_scaling() * mul)
                if stopped:
                    break
            if not stopped:
                self.value = FractionScaledMatrix(
                    scales, scaling=self.value.scaling)
                self._element_reduced_notif(unreduced_size // self.value.size)
                return
