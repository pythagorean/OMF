class MatrionStringMixin:
    def __str__(self):
        super_str = super().__str__()
        return f"Matrion {super_str}"

    def __repr__(self):
        return f"Matrion({self._repr_interior()})"
