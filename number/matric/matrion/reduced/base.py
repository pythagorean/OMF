from typing import List, Tuple, Type, Dict
from typing_extensions import Annotated
from pydantic import BaseModel, Field, model_validator

from number.matric.matrion.core.base import CoreMatrion

from number.matric.matrion.reduced.__init__ import ReducedMatrionInitMixin
from number.matric.matrion.reduced.str import ReducedMatrionStrMixin
from number.matric.matrion.reduced.ops import ReducedMatrionOpsMixin
from number.matric.matrion.reduced.norm import ReducedMatrionNormMixin

from number.matric.matrion.transform.reduction.base import ReductionTransform, DeferTransform
from number.matric.matrion.transform.reduction.diagonal.block import BlockDiagonalReduction
from number.matric.matrion.transform.reduction.diagonal.element import ElementDiagonalReduction
from number.matric.matrion.transform.reduction.radical.factor import RadicalFactoredReduction

ScalingFactor = Annotated[int, Field(gt=1)]


class ReducedMatrion(ReducedMatrionInitMixin,
                     ReducedMatrionStrMixin,
                     ReducedMatrionOpsMixin,
                     ReducedMatrionNormMixin,
                     CoreMatrion,
                     BaseModel):
    reduced: bool = Field(default=False)
    reductions: List[Type[ReductionTransform]] = Field(
        default=[BlockDiagonalReduction, ElementDiagonalReduction, RadicalFactoredReduction])
    perform_reductions: List[Tuple[Type[ReductionTransform],
                                   ScalingFactor]] = Field(default=[])

    # Autopopulated
    reduction_names: Dict[str, Type[ReductionTransform]] = Field(default={})
    defers: Dict[DeferTransform, Type[ReductionTransform]] = Field(default={})

    @model_validator(mode='after')
    def autopopulate_reduction_dictionaries(self):
        if self.reduction_names:
            raise ValueError("The reduction names are populated automatically")
        if self.defers:
            raise ValueError("The defers are populated automatically")
        self._init_autopopulate_reduction_dictionaries()
        return self

    def data(self):
        exported = super().data()
        exported["perform_reductions"] = [(reduction.__name__, scaling)
                                          for reduction, scaling in self.perform_reductions]
        exclude_keys = ["reductions", "reduction_names", "defers"]
        for key in exclude_keys:
            exported.pop(key, None)
        return exported
