from matrix.square.row_view import SquareMatrixRowView


class IntegerSquareMatrixRowView(SquareMatrixRowView):
    def __repr__(self):
        matrix, row = self.parent.matrix, self.row
        row_content = matrix[row]
        return f"IntegerSquareMatrixRowView({row_content})"
