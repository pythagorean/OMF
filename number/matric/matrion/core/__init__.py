from matrix.square.integer.scaled.base import FractionScaledMatrix


class CoreMatrionInitMixin:
    def __init__(self, value, *, scaling=1, normalize=True, **kwargs):
        if isinstance((other := value), self.__class__):
            super().__init__(value=other.value * scaling, **kwargs)
        else:
            scaled_matrix = FractionScaledMatrix(value, scaling=scaling)
            super().__init__(value=scaled_matrix, **kwargs)
        if normalize:
            self._normalize()
