class SecureMatrionOpsMixin:
    def copy(self, **kwargs):
        exclude_keys = ["copy_reductions", "copy_units"]
        for key in exclude_keys:
            if kwargs.get(key) is not False:
                raise ValueError(
                    "{key} must be set to False for secure matrions")
        exclude = {key: False for key in exclude_keys}
        return super().copy(**exclude, **kwargs)
