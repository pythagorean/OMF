from typing import List, Tuple, Type, Dict
from typing_extensions import Annotated
from pydantic import BaseModel, Field, model_validator

from number.matric.matrion.core.base import CoreMatrion

from number.matric.matrion.reduced.__init__ import ReducedMatrionInitMixin
from number.matric.matrion.reduced.str import ReducedMatrionStrMixin
from number.matric.matrion.reduced.ops import ReducedMatrionOpsMixin
from number.matric.matrion.reduced.norm import ReducedMatrionNormMixin

from number.matric.matrion.methods.reduction.base import ReductionMethod, DeferMethod
from number.matric.matrion.methods.reduction.diagonal.block import BlockDiagonalReduction
from number.matric.matrion.methods.reduction.diagonal.element import ElementDiagonalReduction
from number.matric.matrion.methods.reduction.radical.factor import RadicalFactoredReduction

ScalingFactor = Annotated[int, Field(gt=1)]


class ReducedMatrion(ReducedMatrionInitMixin,
                     ReducedMatrionStrMixin,
                     ReducedMatrionOpsMixin,
                     ReducedMatrionNormMixin,
                     CoreMatrion,
                     BaseModel):
    reduced: bool = Field(default=False)
    methods: List[Type[ReductionMethod]] = Field(
        default=[BlockDiagonalReduction, ElementDiagonalReduction, RadicalFactoredReduction])
    applied: List[Tuple[Type[ReductionMethod],
                        ScalingFactor]] = Field(default=[])

    # Autopopulated
    method_names: Dict[str, Type[ReductionMethod]] = Field(default={})
    defers: Dict[DeferMethod, Type[ReductionMethod]] = Field(default={})

    @model_validator(mode='after')
    def autopopulate_dictionaries(self):
        if self.method_names:
            raise ValueError("The method names are populated automatically")
        if self.defers:
            raise ValueError("The defers are populated automatically")
        self._init_autopopulate_dictionaries()
        return self
