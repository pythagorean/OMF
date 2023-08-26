from typing import List
from pydantic import BaseModel

from matrix.square.base import SquareMatrix

from matrix.square.integer.str import IntegerSquareMatrixStrMixin
from matrix.square.integer.ops import IntegerSquareMatrixOpsMixin


class IntegerSquareMatrix(IntegerSquareMatrixStrMixin,
                          IntegerSquareMatrixOpsMixin,
                          SquareMatrix,
                          BaseModel):
    matrix: List[List[int]]
