from typing import TypeVar, List
from pydantic import BaseModel

from matrix.ops import MatrixOpsMixin

T = TypeVar('T')


class Matrix(MatrixOpsMixin,
             BaseModel):
    matrix: List[List[T]]

    def matrix_as_flat_list(self):
        return [item for sublist in self.matrix for item in sublist]

    def __new__(cls, *args, **kwargs):
        if cls is Matrix:
            raise TypeError(
                "Matrix class cannot be instantiated directly")
        return super(Matrix, cls).__new__(cls)
