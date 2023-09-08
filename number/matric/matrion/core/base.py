from pydantic import BaseModel

from number.matric.matrion.core.__init__ import CoreMatrionInitMixin
from number.matric.matrion.core.str import CoreMatrionStrMixin
from number.matric.matrion.core.ops import CoreMatrionOpsMixin


from number.matric.base import MatricNumber
from matrix.square.integer.scaled.base import FractionScaledMatrix


class CoreMatrion(CoreMatrionInitMixin,
                  CoreMatrionStrMixin,
                  CoreMatrionOpsMixin,
                  MatricNumber,
                  BaseModel):
    value: FractionScaledMatrix

    def _normalize(self):
        pass

    def data(self):
        return vars(self)

    @classmethod
    def load(cls, data_dict):
        return cls(**data_dict)
