from number.matric.matrion.methods.reduction.base import ReductionMethod, DeferMethod


class ReducedMatrionOpsMixin:
    def root(self, order):
        matrion = self.copy()
        if DeferMethod.ROOT in self.defers:
            defer_root = self.defers[DeferMethod.ROOT]
            matrion.applied.append((defer_root, order))
        else:
            matrion.value = super().root(order).value
        return matrion

    def add_and_remove_methods(self, *, add_methods=[], remove_methods=[], remove_all=False):
        addition_list = self._validate_method_addition_list(add_methods)
        if remove_all:
            if remove_methods:
                raise ValueError(
                    "You supplied a list of methods to remove, along with remove all")
            removal_list = self.methods
            self.methods.clear()
        else:
            removal_list = self._validate_method_removal_list(remove_methods)
            for method in removal_list:
                self.methods.remove(method)
        self.methods.extend(addition_list)
        if self.reduced:
            previously_applied = [applied[0] for applied in self.applied]
            if addition_list or any(removed_method in previously_applied
                                    for removed_method in removal_list):
                self.value = self._denormalized()
                self.reduced = False
                self.applied = []
                self._normalize()

    def add_methods(self, methods):
        if not isinstance(methods, list):
            raise ValueError("Must supply ReductionMethod list")
        self.add_and_remove_methods(add_methods=methods)

    def remove_methods(self, methods):
        if not isinstance(methods, list):
            raise ValueError("Must supply list of reduction methods to remove")
        self.add_and_remove_methods(remove_methods=methods)

    def add_method(self, method):
        self.add_methods([method])

    def remove_method(self, method):
        self.remove_methods([method])

    def _validate_method_addition_list(self, methods):
        for method in methods:
            if not issubclass(method, ReductionMethod):
                raise ValueError("Must supply valid ReductionMethod")
            if method in self.methods:
                raise ValueError(
                    f"Method {method.__name__} is already installed")
        return methods

    def _validate_method_removal_list(self, methods):
        removal_list = []
        for method in methods:
            installed_method = self._resolve_method(method)
            removal_list.append(installed_method)
        return removal_list

    def _resolve_method(self, method):
        if isinstance(method, str):
            return self._get_method_by_name(method)
        else:
            return self._get_method_by_object(method)

    def _get_method_by_name(self, name):
        if (method := self.method_names.get(name, None)) is None:
            raise ValueError(f"Method {name} is not currently installed")
        return method

    def _get_method_by_object(self, method):
        if not method in self.methods:
            raise ValueError(f"Method {method} is not currently installed")
        return method
