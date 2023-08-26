from pydantic import BaseModel

from number.matrix.__init__ import MatrixNumberInitMixin
from number.matrix.str import MatrixNumberStrMixin
from number.matrix.ops import MatrixNumberOpsMixin
from number.matrix.norm import MatrixNumberNormMixin


from number.base import BaseNumber
from matrix.square.integer.scaled.base import FractionScaledMatrix


class MatrixNumber(MatrixNumberInitMixin,
                   MatrixNumberStrMixin,
                   MatrixNumberOpsMixin,
                   MatrixNumberNormMixin,
                   BaseNumber,
                   BaseModel):
    value: FractionScaledMatrix
