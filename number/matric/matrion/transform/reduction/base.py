from enum import Enum, auto
from number.matric.matrion.transform.base import MatrionTransform


class DeferTransform(Enum):
    ROOT = auto()


class ReductionTransform(MatrionTransform):
    @classmethod
    def normalize(cls, matrion):
        # Subclasses can return True, (int > 1) to record a transformation
        return False

    @classmethod
    def denormalized(cls, matrion, factor):
        # Subclasses can detransform to the original FractionScaledMatrix
        return matrion.value

    @classmethod
    def annotation(cls, factor):
        # Subclasses can return annotation for display
        return None
