from matrix.square.integer.row_view import IntegerSquareMatrixRowView


class FractionScaledMatrixRowView(IntegerSquareMatrixRowView):
    def __repr__(self):
        row_content = self._get_scaled_row()
        return f"FractionScaledMatrixRowView({row_content})"

    def __str__(self):
        row_content = " ".join(str(value) for value in self._get_scaled_row())
        return f"Row: {row_content}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            self_row_content = self._get_scaled_row()
            other_row_content = other._get_scaled_row()
            return self_row_content == other_row_content
        elif isinstance(other, list):
            row_content = self._get_scaled_row()
            return row_content == other
        else:
            return NotImplemented

    def _get_scaled_row(self):
        matrix, row = self.parent.matrix, self.row
        scaling = self.parent.get_scaling()
        return [element * scaling for element in matrix[row]]
