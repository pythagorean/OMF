from fractions import Fraction
from typing import Tuple
from typing_extensions import Annotated
from pydantic import BaseModel, Field

from matrix.square.integer.scaled.__init__ import FractionScaledMatrixInitMixin
from matrix.square.integer.scaled.str import FractionScaledMatrixStrMixin
from matrix.square.integer.scaled.ops import FractionScaledMatrixOpsMixin
from matrix.square.integer.scaled.norm import FractionScaledMatrixNormMixin
from matrix.square.integer.scaled.util import FractionScaledMatrixUtilMixin

from matrix.square.integer.base import IntegerSquareMatrix

PositiveInt = Annotated[int, Field(gt=0)]


class FractionScaledMatrix(FractionScaledMatrixInitMixin,
                           FractionScaledMatrixStrMixin,
                           FractionScaledMatrixOpsMixin,
                           FractionScaledMatrixNormMixin,
                           FractionScaledMatrixUtilMixin,
                           IntegerSquareMatrix,
                           BaseModel):
    """
    Inherits an integer square matrix and adds a scaling factor. The scaling factor
    is stored as a tuple of integers (numerator, denominator) for compatibility
    with Pydantic, and can be converted to a Fraction object for easier manipulation.
    """
    scaling: Tuple[int, PositiveInt]
    reduced: bool

    def get_scaling(self):
        return Fraction(*self.scaling)

    def set_scaling(self, scaling):
        if isinstance(scaling, Fraction):
            self.scaling = scaling.as_integer_ratio()
        elif isinstance(scaling, tuple):
            self.scaling = scaling
