from pydantic import BaseModel

from number.matric.matrion.str import MatrionStrMixin

from number.matric.matrion.unit.base import UnitMatrion as MatrionBase


class Matrion(MatrionStrMixin,
              MatrionBase,
              BaseModel):
    pass
