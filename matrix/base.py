from typing import TypeVar, List
from pydantic import BaseModel, Field
from importlib import import_module

from matrix.ops import MatrixOpsMixin

T = TypeVar('T')


class Matrix(MatrixOpsMixin,
             BaseModel):
    matrix_type: str = Field(default="list")
    matrix: List[List[T]]

    def to_ndarray(self):
        if self.matrix_type == "list":
            np = import_module('numpy')
            self.matrix = np.array(self.matrix)
            self.matrix_type = "ndarray"
        elif self.matrix_type == "ndarray":
            return
        else:
            raise TypeError("Cannot convert non-list matrix to ndarray type")

    def matrix_as_flat_list(self):
        return [item for sublist in self.matrix for item in sublist]

    def __new__(cls, *args, **kwargs):
        if cls is Matrix:
            raise TypeError(
                "Matrix class cannot be instantiated directly")
        return super(Matrix, cls).__new__(cls)
