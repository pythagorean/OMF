class ReducedMatrionStrMixin:
    def __str__(self):
        super_str = super().__str__()
        if not self.perform_reductions:
            return super_str
        total_factor = 1
        for _, factor in self.perform_reductions:
            total_factor *= factor
        now_size = self.value.size
        old_size = now_size * total_factor
        now_str = f"{now_size}x{now_size}"
        old_str = f"{old_size}x{old_size}"
        reduction_str = f"[Reduced: {now_str} from {old_str}]"
        return f"{super_str}\n{reduction_str}"

    def _str_interior(self):
        interior = super()._str_interior()
        annotations = [annotation
                       for annotation in [reduction.annotation(factor)
                                          for reduction, factor in self.perform_reductions]
                       if isinstance(annotation, str)]
        annotations = ' '.join(reversed(annotations))
        if annotations:
            interior = f'{annotations}\n{interior}'
        return interior

    def __repr__(self):
        return f"ReducedMatrion({self._repr_interior()})"

    def _repr_interior(self):
        super_repr = super()._repr_interior()
        if not self.perform_reductions:
            return f"{super_repr}, reduced={self.reduced}"

        perform_repr = ", ".join(
            f"('{reduction.__name__}', {factor})" for reduction, factor in self.perform_reductions)
        return f"{super_repr}, reduced={self.reduced}, perform_reductions=[{perform_repr}]"
