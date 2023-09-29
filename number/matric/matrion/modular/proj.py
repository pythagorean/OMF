from ..core.base import CoreMatrion


class ModularMatrionProjectionMixin:
    def fractional_projector(self, initial_depth=16):
        return CoreMatrion(self._denormalized()).fractional_projector(initial_depth)

    def decimal_projection(self, decimal_places=10):
        return CoreMatrion(self._denormalized()).decimal_projection(decimal_places)
