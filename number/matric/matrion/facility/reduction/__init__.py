from typing import ClassVar
from warnings import warn

from ...transform.reduction.base import DeferTransform


class ReducedMatrionInitMixin:
    suppress_copy_warnings: ClassVar[bool] = False

    def __init__(self, value, *,
                 performed_reductions=None, only_reductions=None, copy_reductions=False, normalize=True,
                 **kwargs):
        if isinstance(value, self.__class__):
            if performed_reductions:
                raise ValueError("Cannot add more performed_reductions here")
            if only_reductions is not None:
                raise ValueError("Cannot specify only_reductions here")
            self._init_reduced_from_self_class(
                value, copy_reductions, **kwargs)
        else:
            self._init_reduced_from_value(
                value, performed_reductions, only_reductions, **kwargs)
        if normalize:
            self._normalize()

    def _init_reduced_from_self_class(self, other, copy_reductions, **kwargs):
        init_args = {
            'reduced': other.reduced,
            **kwargs
        }
        if copy_reductions:
            if other.reductions and not self.suppress_copy_warnings:
                warn("Using copy_reductions might inject unwanted code.")
            init_args['reductions'] = other.reductions
        super().__init__(other, performed_reductions=[], normalize=False, **init_args)
        for reduction, factor, extra in other.performed_reductions:
            reduction = self._get_reduction_by_object(reduction)
            self.performed_reductions.append((reduction, factor, extra))

    def _init_reduced_from_value(self, value, performed_reductions, only_reductions, **kwargs):
        super().__init__(value, performed_reductions=[], normalize=False, **kwargs)
        if not isinstance(only_reductions, list):
            if only_reductions is not None:
                raise ValueError(
                    "If only_reductions are supplied it should be a list")
        else:
            self._init_keep_reductions(only_reductions)
        self._init_performed_reductions(performed_reductions)

    def _init_keep_reductions(self, only_reductions):
        keep_reductions = []
        for reduction_name in only_reductions:
            reduction = self._get_reduction_by_name(reduction_name)
            keep_reductions.append(reduction)
        self.reductions = keep_reductions

    def _init_performed_reductions(self, performed_reductions):
        if performed_reductions is None:
            self.performed_reductions = []
            return
        if not isinstance(performed_reductions, list):
            raise ValueError("Performed reductions list error")
        accepted = []
        for performing in performed_reductions:
            reduction, factor, extra = self._init_validate_performing(
                performing)
            installed_reduction = self._resolve_reduction(reduction)
            accepted.append((installed_reduction, factor, extra))
        self.performed_reductions = accepted

    def _init_validate_performing(self, performing):
        if isinstance(performing, tuple):
            match len(performing):
                case 2:
                    reduction, factor = performing
                    extra = {}
                case 3:
                    reduction, factor, extra = performing
        if reduction is None:
            raise ValueError("Performed reduction format error")
        if not (isinstance(factor, int) and factor > 1):
            raise ValueError("Performed reduction factor error")
        return reduction, factor, extra

    def _init_autopopulate_reduction_dictionaries(self):
        for reduction in self.reductions:
            reduction_name = reduction.__name__
            if not getattr(reduction, 'is_deterministic', None) or not getattr(reduction, 'is_reversible', None):
                raise ValueError(
                    f"Reduction {reduction_name} must be deterministic and reversible.")
            if self.reduction_names.setdefault(reduction_name, reduction) is not reduction:
                raise ValueError(
                    f"Reduction {reduction_name} name conflicts with one already installed")
            if DeferTransform.ROOT in getattr(reduction, 'defers_reductions', []):
                if self.defers.setdefault(DeferTransform.ROOT, reduction) is not reduction:
                    installed_name = self.defers[DeferTransform.ROOT].__name__
                    raise ValueError(
                        f"Reduction {reduction_name} 'root' conflicts with {installed_name}")
            if DeferTransform.MULTIPLY in getattr(reduction, 'defers_reductions', []):
                if self.defers.setdefault(DeferTransform.MULTIPLY, reduction) is not reduction:
                    installed_name = self.defers[DeferTransform.MULTIPLY].__name__
                    raise ValueError(
                        f"Reduction {reduction_name} '__mul__' conflicts with {installed_name}")
