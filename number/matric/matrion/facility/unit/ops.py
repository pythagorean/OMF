from ...transform.unit.base import UnitTransform
from ...transform.unit.general.unspecified import UnspecifiedUnit


class UnitMatrionOpsMixin:
    def add_and_remove_units(self, *, add_units=[], remove_units=[], remove_all=False):
        addition_list = self._validate_reduction_addition_list(add_units)
        if remove_all:
            if remove_units:
                raise ValueError(
                    "You supplied a list of units to remove, along with remove all")
            removal_list = self.unit_types
            removal_list.remove(UnspecifiedUnit)
            self.unit_types = [UnspecifiedUnit]
        else:
            removal_list = self._validate_reduction_removal_list(remove_units)
            for reduction in removal_list:
                self.unit_types.remove(reduction)
        self.unit_types.extend(addition_list)

    def add_units(self, unit_types):
        if not isinstance(unit_types, list):
            raise ValueError("Must supply list of unit types")
        self.add_and_remove_units(add_units=unit_types)

    def remove_units(self, unit_types):
        if not isinstance(unit_types, list):
            raise ValueError(
                "Must supply list of unit types to remove")
        self.add_and_remove_units(remove_units=unit_types)

    def add_unit(self, unit_type):
        self.add_units([unit_type])

    def remove_unit(self, unit_type):
        self.remove_units([unit_type])

    def _validate_unit_addition_list(self, unit_types):
        for unit_type in unit_types:
            if not issubclass(unit_type, UnitTransform):
                raise ValueError("Must supply valid UnitTransform")
            if unit_type in self.unit_types:
                raise ValueError(
                    f"Unit {unit_type.__name__} is already installed")
        return unit_types

    def _validate_unit_removal_list(self, unit_types):
        removal_list = []
        for unit_type in unit_types:
            installed_unit = self._resolve_unit(unit_type)
            removal_list.append(installed_unit)
        return removal_list

    def _resolve_unit(self, unit):
        if isinstance(unit, str):
            return self._get_unit_by_name(unit)
        else:
            return self._get_unit_by_object(unit)

    def _get_unit_by_name(self, name):
        if (unit := self.unit_names.get(name, None)) is None:
            raise ValueError(f"Unit {name} is not currently installed")
        return unit

    def _get_unit_by_object(self, unit):
        if not unit in self.unit_types:
            raise ValueError(
                f"Unit {unit} is not currently installed")
        return unit
