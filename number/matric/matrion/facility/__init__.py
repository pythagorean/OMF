class MatrionFacilityInitMixin:
    def __init__(self, value, **kwargs):
        parent = kwargs.pop('parent')
        kwargs['value'] = value
        super().__init__(parent=parent, kwargs=kwargs)
