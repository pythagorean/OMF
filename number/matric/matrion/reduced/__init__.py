from typing import ClassVar
from warnings import warn
from number.matric.matrion.methods.reduction.base import DeferMethod


class ReducedMatrionInitMixin:
    suppress_warnings: ClassVar[bool] = False

    def __init__(self, value, *, applied=None, only_methods=None, copy_methods=False, normalize=True, **kwargs):
        if isinstance(value, self.__class__):
            if applied:
                raise ValueError("Cannot add more applied methods here")
            if only_methods is not None:
                raise ValueError("Cannot specify only_methods here")
            self._init_from_self_class(value, copy_methods, **kwargs)
        else:
            self._init_from_value(value, applied, only_methods, **kwargs)
        if normalize:
            self._normalize()

    def _init_from_self_class(self, other, copy_methods, **kwargs):
        init_args = {
            'reduced': other.reduced,
            **kwargs
        }
        if copy_methods:
            if other.methods and not self.suppress_warnings:
                warn("Using copy_methods might inject unwanted code.")
            init_args['methods'] = other.methods
        super().__init__(other, applied=[], normalize=False, **init_args)
        for method, factor in other.applied:
            method = self._get_method_by_object(method)
            self.applied.append((method, factor))

    def _init_from_value(self, value, applied, only_methods, **kwargs):
        super().__init__(value, applied=[], normalize=False, **kwargs)
        if not isinstance(only_methods, list):
            if only_methods is not None:
                raise ValueError(
                    "If only_methods are supplied it should be a list")
        else:
            self._init_keep_methods(only_methods)
        self._init_apply_methods(applied)

    def _init_keep_methods(self, only_methods):
        keep_methods = []
        for method_name in only_methods:
            method = self._get_method_by_name(method_name)
            keep_methods.append(method)
        self.methods = keep_methods

    def _init_apply_methods(self, applied):
        if applied is None:
            self.applied = []
            return
        if not isinstance(applied, list):
            raise ValueError("Applied reduction method list error")
        accepted = []
        for applying in applied:
            method, factor = self._init_validate_applying(applying)
            installed_method = self._resolve_method(method)
            accepted.append((installed_method, factor))
        self.applied = accepted

    def _init_validate_applying(self, applying):
        if not isinstance(applying, tuple) or len(applying) != 2:
            raise ValueError("Applied reduction method format error")
        method, factor = applying
        if not (isinstance(factor, int) and factor > 1):
            raise ValueError("Applied reduction factor format error")
        return method, factor

    def _init_autopopulate_dictionaries(self):
        for method in self.methods:
            method_name = method.__name__
            if not getattr(method, 'is_deterministic', None) or not getattr(method, 'is_reversible', None):
                raise ValueError(
                    f"Method {method_name} must be deterministic and reversible.")
            if self.method_names.setdefault(method_name, method) is not method:
                raise ValueError(
                    f"Method {method_name} name conflicts with one already installed")
            if DeferMethod.ROOT in getattr(method, 'defers_methods', []):
                if self.defers.setdefault(DeferMethod.ROOT, method) is not method:
                    installed_name = self.defers[DeferMethod.ROOT].__name__
                    raise ValueError(
                        f"Method {method_name} 'root' conflicts with {installed_name}")
