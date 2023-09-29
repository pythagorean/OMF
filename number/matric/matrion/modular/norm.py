class ModularMatrionNormMixin:
    def _managed_normalize(self, *, called_from=None):
        self._method_attrib_manager('_normalize', called_from)
