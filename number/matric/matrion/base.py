from pydantic import BaseModel

from number.matric.matrion.__init__ import MatrionInitMixin
from number.matric.matrion.str import MatrionStrMixin
from number.matric.matrion.ops import MatrionOpsMixin
from number.matric.matrion.norm import MatrionNormMixin


from number.matric.base import MatricNumber
from matrix.square.integer.scaled.base import FractionScaledMatrix


class Matrion(MatrionInitMixin,
              MatrionStrMixin,
              MatrionOpsMixin,
              MatrionNormMixin,
              MatricNumber,
              BaseModel):
    value: FractionScaledMatrix
    reduced: bool
