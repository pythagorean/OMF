from warnings import warn

from number.matric.matrion.transform.unit.base import UnitTransform


class UnitMatrionInitMixin:
    def __init__(self, value, *,
                 unit=None, only_units=None, copy_units=False, normalize=True,
                 **kwargs):
        if isinstance(value, self.__class__):
            if unit:
                raise ValueError("Cannot add new unit here")
            if only_units is not None:
                raise ValueError("Cannot specify only_units here")
            self._init_unit_from_self_class(value, copy_units, **kwargs)
        else:
            self._init_unit_from_value(value, unit, only_units, **kwargs)
        if normalize:
            self._normalize()

    def _init_unit_from_self_class(self, other, copy_units, **kwargs):
        init_args = kwargs
        if copy_units:
            if other.units and not self.suppress_copy_warnings:
                warn("Using copy_units might inject unwanted code.")
            init_args['units'] = other.units
        super().__init__(other, normalize=False, **init_args)
        self.unit = self._get_unit_by_object(other.unit)

    def _init_unit_from_value(self, value, unit, only_units, **kwargs):
        super().__init__(value, normalize=False, **kwargs)
        if not isinstance(only_units, list):
            if only_units is not None:
                raise ValueError(
                    "If only_units are supplied it should be a list")
        else:
            self._init_keep_units(only_units)
        self._init_apply_unit(unit)

    def _init_keep_units(self, only_units):
        keep_units = []
        for unit_name in only_units:
            unit = self._get_unit_by_name(unit_name)
            keep_units.append(unit)
        self.unit_types = keep_units

    def _init_apply_unit(self, unit):
        if unit is None:
            unit = "unspecified"
        validated_unit = self._init_validate_unit(unit)
        installed_unit = self._resolve_unit(validated_unit)
        self.unit = installed_unit

    def _init_validate_unit(self, unit):
        if not isinstance(unit, (str, UnitTransform)):
            raise ValueError("Unit format error")
        return unit

    def _init_autopopulate_unit_dictionary(self):
        for unit_type in self.unit_types:
            unit_type_name = unit_type.__name__
            unit_name = getattr(unit_type, 'name', None)
            if not isinstance(unit_name, str):
                raise ValueError(f"Unit {unit_type_name} must be named")
            if self.unit_names.setdefault(unit_name, unit_type) is not unit_type:
                raise ValueError(
                    f"Unit {unit_name} name conflicts with one already installed")
