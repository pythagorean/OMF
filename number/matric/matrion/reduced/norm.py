class ReducedMatrionNormMixin:
    def _normalize(self):
        if self.reduced:
            return
        super()._normalize()
        self.reduced = True
        if self.value.size == 1:
            return
        for method in self.methods:
            result = method.normalize(self)
            if isinstance(result, tuple) and len(result) == 2:
                applied = result[0]
                if applied:
                    factor = result[1]
                    self.applied.append((method, factor))

    def _denormalized(self):
        if not self.reduced:
            return self.value
        matrion = self
        for applied in reversed(self.applied):
            method, factor = applied
            result = method.denormalized(matrion, factor)
            matrion = self.__class__(result, normalize=False)
        return matrion.value
