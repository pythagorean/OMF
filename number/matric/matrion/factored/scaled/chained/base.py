from enum import Enum, auto
from typing import List
from pydantic import BaseModel, Field

from number.matric.matrion.factored.scaled.base import VirtualScaledMatrion


class Operator(Enum):
    ADD = auto()
    MULT = auto()


class ChainedMatrion(VirtualScaledMatrion,
                     BaseModel):
    sequence: List[VirtualScaledMatrion] = Field(..., min_items=1)
    operation: Operator
