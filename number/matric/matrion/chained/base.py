from enum import Enum, auto
from typing import List
from pydantic import BaseModel, Field

from number.matric.matrion.base import Matrion


class Operator(Enum):
    ADD = auto()
    MULT = auto()


class ChainedMatrion(Matrion,
                     BaseModel):
    sequence: List[Matrion] = Field(..., min_items=1)
    operation: Operator
