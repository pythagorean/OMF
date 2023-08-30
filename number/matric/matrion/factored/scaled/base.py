from enum import Enum, auto
from typing import List, Tuple
from typing_extensions import Annotated
from pydantic import BaseModel, Field

from number.matric.matrion.factored.scaled.norm import VirtualScaledMatrionNormMixin

from number.matric.matrion.factored.base import RadicalFactoredMatrion

ScalingFactor = Annotated[int, Field(gt=1)]


class Reduced(Enum):
    BLOCK_DIAGONAL = auto()
    ELEMENT_DIAGONAL = auto()


class VirtualScaledMatrion(VirtualScaledMatrionNormMixin,
                           RadicalFactoredMatrion,
                           BaseModel):

    reductions: List[Tuple[Reduced, ScalingFactor]
                     ] = Field(default_factory=list)
