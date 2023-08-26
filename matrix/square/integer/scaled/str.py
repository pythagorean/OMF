from math import gcd


class FractionScaledMatrixStrMixin:
    def __repr__(self):
        matrix_str = str(self.matrix)
        scaling = self.scaling
        if scaling == (1, 1):
            return f"FractionScaledMatrix({matrix_str})"
        scaling_str = str(scaling)
        return f"FractionScaledMatrix({matrix_str}, scaling={scaling_str})"

    def __str__(self):
        scaled_matrix = self._str_scale_matrix()
        max_lengths, formatted_matrix = self._str_format_matrix(
            scaled_matrix)
        return "\n".join(
            [
                " ".join(
                    element.rjust(max_lengths[i])
                    for i, element in enumerate(row)
                )
                for row in formatted_matrix
            ]
        )

    def _str_scale_matrix(self):
        numerator, denominator = self.scaling
        return [
            [
                element * numerator // denominator
                if (product := element * numerator) % denominator == 0
                else (product // (product_gcd := gcd(product, denominator)),
                      denominator // product_gcd)
                for element in row
            ]
            for row in self.matrix
        ]

    def _str_format_matrix(self, matrix):
        formatted_matrix = [
            [
                str(element) if isinstance(
                    element, int) else f"{element[0]}/{element[1]}"
                for element in row
            ]
            for row in matrix
        ]
        max_lengths = [
            max(len(element) for element in column)
            for column in zip(*formatted_matrix)
        ]
        return max_lengths, formatted_matrix

    def as_str(self):
        scaled_matrix = self._str_scale_matrix()
        if self.scaling[1] == 1:
            return "[" + "; ".join(
                [
                    " ".join(str(element) for element in row)
                    for row in scaled_matrix
                ]
            ) + "]"
        else:
            return "[" + "; ".join(
                [
                    " ".join(
                        f"({element[0]}/{element[1]})" if isinstance(element,
                                                                     tuple) else f"({element}/1)"
                        for element in row
                    )
                    for row in scaled_matrix
                ]
            ) + "]"

    @classmethod
    def from_str(cls, string, scaling=(1, 1), normalize=True):
        string = string.strip("[]")
        rows = string.split(";")
        matrix = [
            [
                tuple(map(int, element.strip("()").split("/")))
                if "/" in element else int(element)
                for element in row.replace(",", " ").split()
            ]
            for row in rows
        ]
        if all(isinstance(element, int) for row in matrix for element in row):
            matrix = [[int(element) for element in row] for row in matrix]
        else:
            matrix = [[tuple(map(int, (element, 1))) if isinstance(
                element, int) else element for element in row] for row in matrix]
        return cls(matrix, scaling, normalize)
