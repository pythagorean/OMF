from pydantic import BaseModel

from .string import MatrionStringMixin

from .modular.base import ModularMatrion as MatrionBase


class Matrion(MatrionStringMixin,
              MatrionBase,
              BaseModel):

    @classmethod
    def load(cls, data_dict):
        return cls(**data_dict)

    def copy(self):
        return self.model_copy()
