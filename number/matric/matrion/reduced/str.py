class ReducedMatrionStrMixin:
    def __str__(self):
        super_str = super().__str__()
        if not self.applied:
            return super_str
        total_reduction = 1
        for _, reduction in self.applied:
            total_reduction *= reduction
        now_size = self.value.size
        old_size = now_size * total_reduction
        now_str = f"{now_size}x{now_size}"
        old_str = f"{old_size}x{old_size}"
        reduction_str = f"[Reduced: {now_str} from {old_str}]"
        return f"{super_str}\n{reduction_str}"

    def _str_interior(self):
        interior = super()._str_interior()
        annotations = [annotation
                       for annotation in [method.annotation(reduction)
                                          for method, reduction in self.applied]
                       if isinstance(annotation, str)]
        annotations = ' '.join(reversed(annotations))
        if annotations:
            interior = f'{annotations}\n{interior}'
        return interior

    def __repr__(self):
        return f"ReducedMatrion({self._repr_interior()})"

    def _repr_interior(self):
        super_repr = super()._repr_annotations()
        if not self.applied:
            return f"{super_repr}, reduced={self.reduced}"

        applied_repr = ", ".join(
            f"('{method.__name__}', {reduction})" for method, reduction in self.applied)
        return f"{super_repr}, reduced={self.reduced}, applied=[{applied_repr}]"
