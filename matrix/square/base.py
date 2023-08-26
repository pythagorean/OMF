from pydantic import BaseModel

from matrix.square.__init__ import SquareMatrixInitMixin
from matrix.square.str import SquareMatrixStrMixin
from matrix.square.ops import SquareMatrixOpsMixin

from matrix.base import Matrix


class SquareMatrix(SquareMatrixInitMixin,
                   SquareMatrixStrMixin,
                   SquareMatrixOpsMixin,
                   Matrix,
                   BaseModel):
    size: int

    def __new__(cls, *args, **kwargs):
        if cls is SquareMatrix:
            raise TypeError(
                "SquareMatrix class cannot be instantiated directly")
        return super(SquareMatrix, cls).__new__(cls)
