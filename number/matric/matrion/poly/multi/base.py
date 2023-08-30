from fractions import Fraction
from typing import List, Tuple
from pydantic import BaseModel, Field

from number.matric.matrion.poly.base import PolyMatrion


class Term(BaseModel):
    coefficient: PolyMatrion
    powers: Tuple[Fraction, ...]


class MultiPolyMatrion(BaseModel):
    terms: List[Term] = Field(..., min_items=1)
