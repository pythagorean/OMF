from typing import Type, List, Dict
from pydantic import BaseModel, Field, model_validator

from number.matric.matrion.reduced.base import ReducedMatrion

from number.matric.matrion.unit.__init__ import UnitMatrionInitMixin
from number.matric.matrion.unit.ops import UnitMatrionOpsMixin

from number.matric.matrion.transform.unit.base import UnitTransform
from number.matric.matrion.transform.unit.general.unspecified import UnspecifiedUnit


class UnitMatrion(UnitMatrionInitMixin,
                  UnitMatrionOpsMixin,
                  ReducedMatrion,
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

    def data(self):
        exported = super().data()
        exported["unit"] = self.unit.name
        exclude_keys = ["unit_types", "unit_names"]
        for key in exclude_keys:
            exported.pop(key, None)
        return exported
