from pydantic import BaseModel

from .__init__ import CoreMatrionInitMixin
from .string import CoreMatrionStringMixin
from .ops import CoreMatrionOpsMixin


from number.matric.base import MatricNumber
from matrix.square.integer.scaled.base import FractionScaledMatrix


class CoreMatrion(CoreMatrionInitMixin,
                  CoreMatrionStringMixin,
                  CoreMatrionOpsMixin,
                  MatricNumber,
                  BaseModel):
    value: FractionScaledMatrix

    @classmethod
    def load(cls, data_dict):
        return cls(**data_dict)

    def _normalize(self):
        pass
