from fractions import Fraction


class FractionScaledRawOpsMixin:
    @classmethod
    def _zeros_raw(cls, size, set_fractional=False):
        zeros_matrix = super()._zeros_raw(size)
        if set_fractional:
            zeros_matrix[0][0] = Fraction(0)
        return zeros_matrix
