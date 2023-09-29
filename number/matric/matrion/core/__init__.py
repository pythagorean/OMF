from matrix.square.integer.scaled.base import FractionScaledMatrix


class CoreMatrionInitMixin:
    __version__ = '1.0.0'

    def __init__(self, value, *, scaling=1, **kwargs):
        if isinstance((other := value), self.__class__):
            super().__init__(value=other.value * scaling, **kwargs)
        else:
            scaled_matrix = FractionScaledMatrix(value, scaling=scaling)
            super().__init__(value=scaled_matrix, **kwargs)
