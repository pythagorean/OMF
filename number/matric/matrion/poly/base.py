from typing import List, Union, Tuple
from pydantic import BaseModel, Field, validator

from number.matric.matrion.factored.scaled.chained.base import ChainedMatrion, Operator
from number.matric.matrion.factored.scaled.base import VirtualScaledMatrion

from number.matric.matrion.poly.__init__ import PolyMatrionInitMixin


class PolyMatrion(PolyMatrionInitMixin,
                  BaseModel):
    sequence: List[Union[VirtualScaledMatrion, ChainedMatrion, Tuple[
        Operator, Union[VirtualScaledMatrion, ChainedMatrion]]]] = Field(..., min_items=1)

    @validator('sequence')
    def validate_sequence(cls, sequence):
        first_element = sequence[0]
        if isinstance(first_element, tuple):
            raise ValueError("First element cannot be a tuple")
        if len(sequence) > 1:
            for element in sequence[1:]:
                if not isinstance(element, tuple):
                    raise ValueError("Elements after first must be tuples")
        return sequence
