class ModularMatrionStringMixin:
    def __str__(self):
        return self._method_attrib_manager('__str__', called_from=None)

    def _managed_str(self):
        return f"value:\n{self._str_interior()}"

    def _str_interior(self, *, called_from=None):
        return self._method_attrib_manager('_str_interior', called_from)

    def _repr_interior(self, *, called_from=None):
        return self._method_attrib_manager('_repr_interior', called_from)
