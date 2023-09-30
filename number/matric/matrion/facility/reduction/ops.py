from copy import deepcopy

from ...transform.reduction.base import ReductionTransform, DeferTransform


class ReducedMatrionOpsMixin:
    def data(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        exported = super().data(called_from=called_from)
        exclude_keys = ["reductions", "reduction_names", "defers"]
        performed_reductions = []
        for performed_reduction in self.performed_reductions:
            match len(performed_reduction):
                case 2:
                    reduction, scaling = performed_reduction
                    performed_reductions.append((reduction.__name__, scaling))
                case 3:
                    reduction, scaling, extra = performed_reduction
                    if not extra:
                        performed_reductions.append(
                            (reduction.__name__, scaling))
                    else:
                        performed_reductions.append(
                            (reduction.__name__, scaling, extra))
        if not performed_reductions:
            exclude_keys.append("performed_reductions")
        else:
            exported["performed_reductions"] = performed_reductions
        for key in exclude_keys:
            exported.pop(key, None)
        return exported

    def root(self, order):
        selfcopy = deepcopy(self)
        if DeferTransform.ROOT in self.defers:
            defer_root = self.defers[DeferTransform.ROOT]
            selfcopy.performed_reductions.append((defer_root, order))
        else:
            selfcopy.value = super().root(order).value
        return selfcopy.as_matrion()

    def __mul__(self, other):
        if DeferTransform.MULTIPLY in self.defers:
            selfcopy = deepcopy(self)
            defer_multiply = self.defers[DeferTransform.MULTIPLY]
            if defer_multiply.defers(selfcopy, DeferTransform.MULTIPLY, other=other):
                return selfcopy.as_matrion()
        return self._managed_mul(other)

    def add_and_remove_reductions(self, *, add_reductions=[], remove_reductions=[], remove_all=False):
        addition_list = self._validate_reduction_addition_list(add_reductions)
        if remove_all:
            if remove_reductions:
                raise ValueError(
                    "You supplied a list of reductions to remove, along with remove all")
            removal_list = self.reductions
            self.reductions.clear()
        else:
            removal_list = self._validate_reduction_removal_list(
                remove_reductions)
            for reduction in removal_list:
                self.reductions.remove(reduction)
        self.reductions.extend(addition_list)
        if self.reduced:
            previously_performed = [performed[0]
                                    for performed in self.performed_reductions]
            if addition_list or any(removed_reduction in previously_performed
                                    for removed_reduction in removal_list):
                self.value = self._denormalized()
                self.reduced = False
                self.performed_reductions = []
                self._normalize()

    def add_reductions(self, reductions):
        if not isinstance(reductions, list):
            raise ValueError("Must supply ReductionTransform list")
        self.add_and_remove_reductions(add_reductions=reductions)

    def remove_reductions(self, reductions):
        if not isinstance(reductions, list):
            raise ValueError(
                "Must supply list of reduction transforms to remove")
        self.add_and_remove_reductions(remove_reductions=reductions)

    def add_reduction(self, reduction):
        self.add_reductions([reduction])

    def remove_reduction(self, reduction):
        self.remove_reductions([reduction])

    def _validate_reduction_addition_list(self, reductions):
        for reduction in reductions:
            if not issubclass(reduction, ReductionTransform):
                raise ValueError("Must supply valid ReductionTransform")
            if reduction in self.reductions:
                raise ValueError(
                    f"reduction {reduction.__name__} is already installed")
        return reductions

    def _validate_reduction_removal_list(self, reductions):
        removal_list = []
        for reduction in reductions:
            installed_reduction = self._resolve_reduction(reduction)
            removal_list.append(installed_reduction)
        return removal_list

    def _resolve_reduction(self, reduction):
        if isinstance(reduction, str):
            return self._get_reduction_by_name(reduction)
        else:
            return self._get_reduction_by_object(reduction)

    def _get_reduction_by_name(self, name):
        if (reduction := self.reduction_names.get(name, None)) is None:
            raise ValueError(f"reduction {name} is not currently installed")
        return reduction

    def _get_reduction_by_object(self, reduction):
        if not reduction in self.reductions:
            raise ValueError(
                f"Reduction {reduction} is not currently installed")
        return reduction
