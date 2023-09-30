class MatrionFacilityOpsMixin:
    def data(self, *, called_from=None):
        return self.parent._managed_data(called_from=called_from)

    def as_matrion(self):
        from number.matric.matrion.base import Matrion
        return Matrion.load(self.data())

    def eq_exclude(self, exclude):
        self.parent.eq_exclude(exclude)

    def _managed_mul(self, other):
        return self.parent._managed_mul(other)
