from pydantic import BaseModel

from number.matric.matrion.str import MatrionStrMixin

from number.matric.matrion.stamped.base import StampedMatrion as MatrionBase


class Matrion(MatrionStrMixin,
              MatrionBase,
              BaseModel):
    pass
