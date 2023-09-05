class SecureMatrionOpsMixin:
    def copy(self, **kwargs):
        if kwargs.get('copy_methods') is not False:
            raise ValueError(
                "copy_methods must be set to False for secure matrions")
        return super().copy(copy_methods=False, **kwargs)
