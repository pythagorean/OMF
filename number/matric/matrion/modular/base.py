from typing import List, Dict, Tuple, Set, Any
from pydantic import BaseModel, Field

from .__init__ import ModularMatrionInitMixin
from .string import ModularMatrionStringMixin
from .attrib import ModularMatrionAttribMixin
from .ops import ModularMatrionOpsMixin
from .norm import ModularMatrionNormMixin
from .proj import ModularMatrionProjectionMixin

from ..facility.base import MatrionFacility
from ..facility.reduction.base import ReducedMatrion
from ..facility.unit.base import UnitMatrion
from ..facility.stamped.base import StampedMatrion

from ..core.base import CoreMatrion

default_facilities = [ReducedMatrion, UnitMatrion, StampedMatrion]


class ModularMatrion(ModularMatrionInitMixin,
                     ModularMatrionStringMixin,
                     ModularMatrionAttribMixin,
                     ModularMatrionOpsMixin,
                     ModularMatrionNormMixin,
                     ModularMatrionProjectionMixin,
                     BaseModel):
    core: CoreMatrion
    facilities: List[Tuple[MatrionFacility, Set[str]]] = Field(default=[])
    facility_index: Dict[str, int] = Field(default={})
    attrib_values: Dict[str, Any] = Field(default={})
    method_stacks: Dict[str, List[str]] = Field(default={})
    eq_exclusions: Set[str] = Field(default=set())


for facility in default_facilities:
    facility.model_rebuild()
