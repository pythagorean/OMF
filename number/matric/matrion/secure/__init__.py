class SecureMatrionInitMixin:
    def __init__(self, other, **kwargs):
        if kwargs.get('copy_methods') is not False:
            raise ValueError(
                "copy_methods must be set to False for secure matrions")
        super().__init__(other, copy_methods=False, **kwargs)
