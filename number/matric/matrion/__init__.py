from matrix.square.integer.scaled.base import FractionScaledMatrix


class MatrionInitMixin:
    def __init__(self, value, *, scaling=1, normalize=True, **kwargs):
        if isinstance((other := value), self.__class__):
            super().__init__(other.value, reduced=other.reduced,
                             reductions=other.reductions, **kwargs)
        else:
            scaled_matrix = FractionScaledMatrix(value, scaling=scaling)
            super().__init__(value=scaled_matrix, reduced=False, **kwargs)
        if normalize:
            self._normalize()
