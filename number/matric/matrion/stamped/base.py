from time import time_ns
from pydantic import BaseModel, Field, model_validator

from number.matric.matrion.unit.base import UnitMatrion


class StampedMatrion(UnitMatrion,
                     BaseModel):
    core_version: str = Field(default=None)
    creation_time_ns: int = Field(default=None)

    @model_validator(mode='after')
    def stamp_attributes(self):
        self.core_version = self.__version__
        self.creation_time_ns = time_ns()

    def __setattr__(self, name, value):
        if name in ["core_version", "creation_time_ns"]:
            if getattr(self, name) is not None:
                raise AttributeError(
                    "Cannot change read-only field '{name}'")
        super().__setattr__(name, value)

    def __init__(self, value, *, core_version=None, creation_time_ns=None, **kwargs):
        super().__init__(value, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(getattr(self, attr) == getattr(other, attr)
                   for attr in self.__dict__.keys()
                   if attr != 'creation_time_ns')

    def is_identical(self, other):
        return super().__eq__(other)
