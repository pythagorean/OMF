class MatrionFacilityStringMixin:
    def __str__(self):
        return self.parent._managed_str()

    def _str_interior(self, called_from):
        return self.parent._str_interior(called_from=called_from)

    def _repr_interior(self, called_from):
        return self.parent._repr_interior(called_from=called_from)
