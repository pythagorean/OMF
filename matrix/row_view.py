class MatrixRowView:
    def __init__(self, matrix, row):
        self.parent = matrix
        self.row = row

    def __repr__(self):
        matrix, row = self.parent.matrix, self.row
        row_content = matrix[row]
        return f"MatrixRowView({row_content})"

    def __str__(self):
        matrix, row = self.parent.matrix, self.row
        row_content = " ".join(str(value)
                               for value in matrix[row])
        return f"Row: {row_content}"

    def __getitem__(self, col):
        row = self.row
        return self.parent[row, col]

    def __setitem__(self, col, value):
        row = self.row
        self.parent[row, col] = value

    def __eq__(self, other):
        if not isinstance(other, list):
            return NotImplemented
        matrix, row = self.parent.matrix, self.row
        return matrix[row] == other
