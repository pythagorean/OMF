from number.matric.matrion.core.base import CoreMatrion


class ModularMatrionInitMixin:
    def __init__(self, value, **kwargs):
        super().__init__(core=CoreMatrion(value))
        instantiated_facilities = []
        self_attribs = set(attr for attr in dir(self.__class__)
                           if attr != '__fields__' and
                           not callable(getattr(self.__class__, attr)))
        from .base import default_facilities
        for facility in default_facilities:
            instantiated = facility(value, parent=self, **kwargs)
            kwargs, instantiated.kwargs = instantiated.kwargs, None
            value = kwargs.pop('value')
            facility_attribs = set(dir(facility)) - self_attribs
            instantiated_facilities.append((instantiated, facility_attribs))
        self._set_core(CoreMatrion(value, **kwargs))
        self._set_facilities(instantiated_facilities)
        facility_index = self._get_facility_index()
        for facility_indexed in range(len(instantiated_facilities)):
            facility, _ = instantiated_facilities[facility_indexed]
            facility_name = facility.__class__.__name__
            if facility_index.setdefault(facility_name, facility_indexed) is not facility_indexed:
                raise ValueError(
                    f"Facility {facility_name} name conflicts with one already installed")
