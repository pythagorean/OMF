class ReducedMatrionNormMixin:
    def _normalize(self):
        if self.reduced:
            return
        super()._normalize()
        self.reduced = True
        if self.value.size == 1:
            return
        performed = []
        for reduction in self.reductions:
            result = reduction.normalize(self)
            if isinstance(result, tuple) and len(result) == 2:
                should_perform = result[0]
                if should_perform:
                    factor = result[1]
                    performed.append((reduction, factor))
        self.performed_reductions.extend(reversed(performed))

    def _denormalized(self):
        from number.matric.matrion.base import Matrion
        if not self.reduced:
            return self.value
        matrion = self
        for performed in self.performed_reductions:
            reduction, factor = performed
            result = reduction.denormalized(matrion, factor)
            matrion = Matrion(result, normalize=False)
        return matrion.value
