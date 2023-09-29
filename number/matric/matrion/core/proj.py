from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP, localcontext


class CoreMatrionProjectionMixin:
    def _extract_root_and_remainder(self):
        # Retrieve the scaled matrix value and its size
        scaled_value = self.value
        size = scaled_value.size
        # Single-element matrix case
        if size == 1:
            return None, scaled_value[0, 0]
        # Retrieve the raw matrix data
        raw_matrix = scaled_value.matrix
        # Check if all diagonal elements are the same in the raw matrix
        first_diagonal_element = raw_matrix[0][0]
        if all(raw_matrix[i][i] == first_diagonal_element for i in range(1, size)):
            # Zero diagonal case
            if first_diagonal_element == 0:
                return scaled_value, Fraction(0)
            # Non-zero diagonal case
            modified_value = scaled_value.copy()
            for i in range(size):
                modified_value.matrix[i][i] = 0
            return modified_value, scaled_value[0, 0]
        # Different diagonal elements case
        raise ValueError("Multiplied roots cannot be projected yet")

    def fractional_projector(self, initial_depth=16):
        root_value, remainder = self._extract_root_and_remainder()
        # If there's no root matrix, the Matrion is a scalar, yield indefinitely
        if root_value is None:
            while True:
                yield remainder
        # Add identity and raise to initial_depth power for initial projection
        projection = (
            root_value + root_value.identity(root_value.size)) ** initial_depth
        # Generate fractions indefinitely to approximate root convergently
        while True:
            yield Fraction(projection[0, 0], projection[0, 1]) + remainder
            projection *= projection

    def decimal_projection(self, decimal_places=10):
        convergence = self.fractional_projector()
        last_rounded = None
        while (rounded := round(next(convergence), decimal_places)) != last_rounded:
            last_rounded = rounded
        numerator, denominator = last_rounded.as_integer_ratio()
        with localcontext() as ctx:
            ctx.prec = decimal_places + 1
            as_decimal = Decimal(numerator) / Decimal(denominator)
            quantization = Decimal(10) ** -decimal_places
            return as_decimal.quantize(quantization, rounding=ROUND_HALF_UP)
