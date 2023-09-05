from enum import Enum, auto


class DeferMethod(Enum):
    ROOT = auto()


class ReductionMethod:
    # Subclasses need to override these
    is_deterministic = None
    is_reversible = None

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
