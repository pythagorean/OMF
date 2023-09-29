class MatrionFacilityAttribMixin:
    def __setattr__(self, name, value):
        if name in self.__dict__:
            super().__setattr__(name, value)
        else:
            self.parent._managed_set_attrib(name, value)
        if name == "value":
            self.kwargs[name] = value

    def __getattr__(self, name):
        try:
            return self.parent._get_attrib_value(name)
        except AttributeError:
            return self.parent._managed_get_attrib(name)
