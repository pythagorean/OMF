class VirtualScaledMatrionNormMixin:
    def _block_reduced_notif(self, scale):
        from number.matric.matrion.factored.scaled.base import Reduced
        self.reductions.append((Reduced.BLOCK_DIAGONAL, scale))

    def _element_reduced_notif(self, scale):
        from number.matric.matrion.factored.scaled.base import Reduced
        self.reductions.append((Reduced.ELEMENT_DIAGONAL, scale))
