from time import time_ns
from pydantic import BaseModel, Field, model_validator

from ..base import MatrionFacility


class StampedMatrion(MatrionFacility,
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
        super().eq_exclude('creation_time_ns')

    def is_identical(self, other):
        return super().__eq__(other)

    def _repr_interior(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        super_repr = super()._repr_interior(called_from=called_from)
        return f"{super_repr}, core_version='{self.core_version}', creation_time_ns='{self.creation_time_ns}'"

    def __str__(self):
        return super().__str__()

    def _str_interior(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        return super()._str_interior(called_from=called_from)

    def data(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        exported = super().data(called_from=called_from)
        exported["core_version"] = self.core_version
        exported["creation_time_ns"] = self.creation_time_ns
        return exported
