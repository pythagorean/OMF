from .ops import RadicalFactoredReductionOpsMixin
from .norm import RadicalFactoredReductionNormMixin
from ..base import ReductionTransform, DeferTransform


class RadicalFactoredReduction(RadicalFactoredReductionOpsMixin,
                               RadicalFactoredReductionNormMixin,
                               ReductionTransform):
    is_deterministic = True
    is_reversible = True

    defers_reductions = [DeferTransform.ROOT, DeferTransform.MULTIPLY]
