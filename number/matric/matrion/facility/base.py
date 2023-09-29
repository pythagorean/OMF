from typing import TYPE_CHECKING, Dict
from pydantic import BaseModel

from .__init__ import MatrionFacilityInitMixin
from .string import MatrionFacilityStringMixin
from .attrib import MatrionFacilityAttribMixin
from .ops import MatrionFacilityOpsMixin
from .norm import MatrionFacilityNormMixin


if TYPE_CHECKING:
    from ..modular.base import ModularMatrion


class MatrionFacility(MatrionFacilityInitMixin,
                      MatrionFacilityStringMixin,
                      MatrionFacilityAttribMixin,
                      MatrionFacilityOpsMixin,
                      MatrionFacilityNormMixin,
                      BaseModel):
    parent: 'ModularMatrion'
    kwargs: Dict
