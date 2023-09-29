class CoreMatrionStringMixin:
    def __str__(self):
        return f"value:\n{self._str_interior()}"

    def __repr__(self):
        return f"CoreMatrion({self._repr_interior()})"

    def _str_interior(self):
        return self.value.__str__()

    def _repr_interior(self):
        return self.value.__repr__()
