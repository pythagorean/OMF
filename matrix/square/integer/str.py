class IntegerSquareMatrixStrMixin:
    def __repr__(self):
        return f"IntegerSquareMatrix({str(self.matrix)})"

    def __str__(self):
        max_lengths, formatted_matrix = self._str_format_matrix(self.matrix)
        return "\n".join([
            " ".join(
                element.rjust(max_lengths[i])
                for i, element in enumerate(row)
            )
            for row in formatted_matrix
        ])

    def _str_format_matrix(self, matrix):
        formatted_matrix = [
            [str(element) for element in row]
            for row in matrix
        ]
        max_lengths = [
            max(len(element) for element in column)
            for column in zip(*formatted_matrix)
        ]
        return max_lengths, formatted_matrix

    def as_str(self):
        return "[" + "; ".join([
            " ".join(str(element) for element in row)
            for row in self.matrix
        ]) + "]"

    @classmethod
    def from_str(cls, string):
        string = string.strip("[]")
        rows = string.split(";")
        matrix = [
            [
                int(element)
                for element in row.replace(",", " ").split()
            ]
            for row in rows
        ]
        matrix = [[int(element) for element in row] for row in matrix]
        return cls(matrix)
