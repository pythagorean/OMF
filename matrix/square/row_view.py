from matrix.row_view import MatrixRowView


class SquareMatrixRowView(MatrixRowView):
    def __repr__(self):
        matrix, row = self.parent.matrix, self.row
        row_content = matrix[row]
        return f"SquareMatrixRowView({row_content})"
