from fractions import Fraction
from typing import ClassVar


class FractionScaledMatrixInitMixin:
    """
    Initializes a FractionScaledMatrix.

    - If the first element of a list or matrix is an integer, the entire list or matrix must be integers.
    - If the first element is a tuple or fraction, subsequent elements may be mixed integers, fractions,
      or tuples, since integers are subsets of fractions.
    - All elements are normalized to a common scaling numerator and denominator.

    This reflects the mathematical concept that all integers are rational numbers, but not all fractions
    (rational numbers) can be represented as integers.

    floats_enabled: Set to True to enable float input.
    """
    floats_enabled: ClassVar[bool] = False

    def __init__(self, elements, *, scaling=(1, 1), normalize=True, **kwargs):
        first_element = elements
        if isinstance(elements, list) and elements:
            first_element = elements[0]
            if isinstance(first_element, list) and first_element:
                first_element = first_element[0]
        if isinstance(scaling, int):
            scaling = (scaling, 1)
        elif isinstance(scaling, Fraction):
            scaling = scaling.as_integer_ratio()
        if isinstance((other := elements), self.__class__):
            super().__init__(other.matrix, scaling=other.scaling,
                             reduced=other.reduced, **kwargs)
        elif isinstance(first_element, int):
            self._init_from_integers(elements, scaling, **kwargs)
        elif not isinstance(elements, list):
            self._init_from_fraction(elements, scaling, **kwargs)
        elif not isinstance(elements[0], list):
            self._init_from_fraction_list(elements, scaling, **kwargs)
        else:
            self._init_from_fraction_matrix(elements, scaling, **kwargs)
        if normalize:
            self._normalize()

    def _init_from_integers(self, integers, scaling=(1, 1), **kwargs):
        super().__init__(matrix=integers, scaling=scaling, reduced=False, **kwargs)

    def _convert_to_fraction(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            return Fraction(*value)
        elif isinstance(value, float) and not self.floats_enabled:
            raise ValueError("Support for floats is currently disabled")
        else:
            return Fraction(value)

    def _init_from_fraction(self, scalar, scaling=(1, 1), **kwargs):
        scalar = self._convert_to_fraction(scalar)
        scaling = self._convert_to_fraction(scaling)
        scaled = (scalar * scaling).as_integer_ratio()
        super().__init__(matrix=1, scaling=scaled, reduced=True, **kwargs)

    def _init_from_fraction_list(self, fraction_list, scaling=(1, 1), **kwargs):
        fractions = [self._convert_to_fraction(value)
                     for value in fraction_list]
        denominators = [fraction.denominator for fraction in fractions]
        common_denominator = self._lcm_nonzero_elements(*denominators)
        scaled_numerators = [fraction.numerator * common_denominator // fraction.denominator
                             for fraction in fractions]
        scaling = self._convert_to_fraction(scaling) / common_denominator
        super().__init__(
            matrix=scaled_numerators,
            scaling=scaling.as_integer_ratio(),
            reduced=False,
            **kwargs)

    def _init_from_fraction_matrix(self, fraction_matrix, scaling=(1, 1), **kwargs):
        fractions = [[self._convert_to_fraction(value)
                      for value in row] for row in fraction_matrix]
        denominators = [fraction.denominator for row in fractions
                        for fraction in row]
        common_denominator = self._lcm_nonzero_elements(*denominators)
        scaled_numerators = [[fraction.numerator * common_denominator // fraction.denominator
                              for fraction in row] for row in fractions]
        scaling = self._convert_to_fraction(scaling) / common_denominator
        super().__init__(
            matrix=scaled_numerators,
            scaling=scaling.as_integer_ratio(),
            reduced=False,
            **kwargs)
