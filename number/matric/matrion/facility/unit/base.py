from typing import Type, List, Dict
from pydantic import BaseModel, Field, model_validator

from .__init__ import UnitMatrionInitMixin
from .ops import UnitMatrionOpsMixin
from ..base import MatrionFacility

from ...transform.unit.base import UnitTransform
from ...transform.unit.general.unspecified import UnspecifiedUnit


class UnitMatrion(UnitMatrionInitMixin,
                  UnitMatrionOpsMixin,
                  MatrionFacility,
                  BaseModel):
    substance: str = Field(default="unspecified")
    unit: Type[UnitTransform] = Field(default=UnspecifiedUnit)
    unit_types: List[Type[UnitTransform]] = Field(default=[UnspecifiedUnit])

    # Autopopulated
    unit_names: Dict[str, Type[UnitTransform]] = Field(default={})

    @model_validator(mode='after')
    def autopopulate_unit_dictionary(self):
        if self.unit_names:
            raise ValueError("The unit names are populated automatically")
        self._init_autopopulate_unit_dictionary()
        return self

    def data(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        exported = super().data(called_from=called_from)
        exported["unit"] = self.unit.name
        exported["substance"] = self.substance
        exclude_keys = ["unit_types", "unit_names"]
        for key in exclude_keys:
            exported.pop(key, None)
        return exported

    def _repr_interior(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        super_repr = super()._repr_interior(called_from=called_from)
        return f"{super_repr}, unit='{self.unit.name}', substance='{self.substance}'"

    def __str__(self):
        return super().__str__()

    def _str_interior(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        return super()._str_interior(called_from=called_from)
