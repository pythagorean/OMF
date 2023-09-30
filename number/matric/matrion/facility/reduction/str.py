class ReducedMatrionStrMixin:
    def __str__(self):
        super_str = super().__str__()
        if not self.performed_reductions:
            return super_str
        total_factor = 1
        for _, factor in self.performed_reductions:
            total_factor *= factor
        now_size = self.value.size
        old_size = now_size * total_factor
        now_str = f"{now_size}x{now_size}"
        old_str = f"{old_size}x{old_size}"
        reduction_str = f"[Reduced: {now_str} from {old_str}]"
        return f"{super_str}\n{reduction_str}"

    def _str_interior(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        interior = super()._str_interior(called_from=called_from)
        annotations = []
        for performed_reduction in self.performed_reductions:
            reduction, factor, extra = performed_reduction
            if not extra:
                if isinstance(annotation := reduction.annotation(factor), str):
                    annotations.append(annotation)
            else:
                if isinstance(annotation := reduction.annotation(factor, extra=extra), str):
                    annotations.append(annotation)
        if (annotations := ' '.join(reversed(annotations))):
            interior = f'{annotations}\n{interior}'
        return interior

    def __repr__(self):
        return f"ReducedMatrion({self._repr_interior()})"

    def _repr_interior(self, *, called_from=None):
        if not called_from:
            called_from = self.__class__.__name__
        super_repr = super()._repr_interior(called_from=called_from)
        if not self.performed_reductions:
            return f"{super_repr}, reduced={self.reduced}"
        perform_repr = ", ".join(
            f"('{reduction.__name__}', {factor}{'' if not extra else ', ' + str(extra)})"
            for reduction, factor, extra in self.performed_reductions)
        return f"{super_repr}, reduced={self.reduced}, performed_reductions=[{perform_repr}]"
