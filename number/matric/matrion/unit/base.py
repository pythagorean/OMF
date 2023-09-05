from pydantic import BaseModel, Field

from number.matric.matrion.reduced.base import ReducedMatrion


class UnitMatrion(ReducedMatrion,
                  BaseModel):
    unit: str = Field(default=None)
