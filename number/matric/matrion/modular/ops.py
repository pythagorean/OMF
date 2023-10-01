from ..core.base import CoreMatrion


class ModularMatrionOpsMixin:
    def _managed_data(self, *, called_from=None):
        return self._method_attrib_manager('data', called_from)

    def data(self):
        return self._managed_data()

    def eq_exclude(self, exclude):
        if exclude in self.eq_exclusions:
            raise ValueError(
                f"Equality exclusion for attribute '{exclude}' is already set.")
        self.eq_exclusions.add(exclude)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        selfdata, otherdata = self.data(), other.data()
        if (selfkeys := selfdata.keys()) != otherdata.keys():
            return False
        return all(selfdata[key] == otherdata[key]
                   for key in selfkeys
                   if key not in self.eq_exclusions)

    def __mul__(self, other):
        method_name = '__mul__'
        if not (facilities := self._facilities_with_attrib(method_name)):
            return self._managed_mul(other)
        self._get_method_stacks()[method_name] = facilities
        return self._manage_attrib_method(method_name, other=other)

    def _managed_mul(self, other):
        from ..base import Matrion
        if not isinstance(other, (self.__class__, Matrion)):
            return Matrion(CoreMatrion(self._denormalized()) * other)
        return Matrion(CoreMatrion(self._denormalized()) * CoreMatrion(other._denormalized()))
