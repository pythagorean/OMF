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

ScalingFactor = Annotated[int, Field(gt=1)]


class ReducedMatrion(ReducedMatrionInitMixin,
                     ReducedMatrionStrMixin,
                     ReducedMatrionOpsMixin,
                     ReducedMatrionNormMixin,
                     MatrionFacility,
                     BaseModel):
    reduced: bool = Field(default=False)
    reductions: List[Type[ReductionTransform]] = Field(
        default=[BlockDiagonalReduction, ElementDiagonalReduction, RadicalFactoredReduction])
    performed_reductions: List[Tuple[Type[ReductionTransform],
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

    def data(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        exported = super().data(called_from=called_from)
        exclude_keys = ["reductions", "reduction_names", "defers"]
        if not (performed_reductions := [(reduction.__name__, scaling)
                                         for reduction, scaling in self.performed_reductions]):
            exclude_keys.append("performed_reductions")
        else:
            exported["performed_reductions"] = performed_reductions
        for key in exclude_keys:
            exported.pop(key, None)
        return exported
