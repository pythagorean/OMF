from pydantic import BaseModel

from number.base import BaseNumber
from matrix.base import Matrix


class MatricNumber(BaseNumber,
                   BaseModel):
    value: Matrix
