class MatrionFacilityNormMixin:
    def _normalize(self):
        return self.parent._managed_normalize()
