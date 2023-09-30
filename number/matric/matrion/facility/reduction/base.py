from typing import List, Tuple, Type, Dict
from typing_extensions import Annotated
from pydantic import BaseModel, Field, model_validator

from .__init__ import ReducedMatrionInitMixin
from .str import ReducedMatrionStrMixin
from .ops import ReducedMatrionOpsMixin
from .norm import ReducedMatrionNormMixin
from ..base import MatrionFacility

from ...transform.reduction.base import ReductionTransform, DeferTransform
from ...transform.reduction.diagonal.block import BlockDiagonalReduction
from ...transform.reduction.diagonal.element import ElementDiagonalReduction
from ...transform.reduction.radical.factor import RadicalFactoredReduction

default_reductions = [BlockDiagonalReduction,
                      ElementDiagonalReduction,
                      RadicalFactoredReduction]

ScalingFactor = Annotated[int, Field(gt=1)]


class ReducedMatrion(ReducedMatrionInitMixin,
                     ReducedMatrionStrMixin,
                     ReducedMatrionOpsMixin,
                     ReducedMatrionNormMixin,
                     MatrionFacility,
                     BaseModel):
    reduced: bool = Field(default=False)
    reductions: List[
        Type[ReductionTransform]] = Field(default=default_reductions)
    performed_reductions: List[Tuple[
        Type[ReductionTransform], ScalingFactor, Dict]] = Field(default=[])

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
