from typing import TypeVar, List
from pydantic import BaseModel

from number.ops import BaseNumberOpsMixin

T = TypeVar('T')


class BaseNumber(BaseNumberOpsMixin,
                 BaseModel):
    value: T

    def __new__(cls, *args, **kwargs):
        if cls is BaseNumber:
            raise TypeError(
                "BaseNumber class cannot be instantiated directly")
        return super(BaseNumber, cls).__new__(cls)
