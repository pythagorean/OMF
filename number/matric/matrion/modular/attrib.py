class ModularMatrionAttribMixin:
    def _get_core(self):
        return self.__dict__.get('core')

    def _set_core(self, new_core):
        self.__dict__['core'] = new_core

    def _get_facilities(self):
        return self.__dict__.get('facilities')

    def _set_facilities(self, new_facilities):
        self.__dict__['facilities'] = new_facilities

    def _get_facility_index(self):
        return self.__dict__.get('facility_index')

    def _get_facility(self, name):
        facility_indexed = self._get_facility_index().get(name)
        facility, _ = self._get_facilities()[facility_indexed]
        return facility

    def _get_attrib_values(self):
        return self.__dict__.get('attrib_values')

    def _get_method_stacks(self):
        return self.__dict__.get('method_stacks')

    def __setattr__(self, name, value):
        facilities_with_attrib = self._facilities_with_attrib(name)
        if not facilities_with_attrib:
            self._managed_set_attrib(name, value)
        elif len(facilities_with_attrib) > 1:
            conflicting_facilities = [
                type(facility).__name__ for facility in facilities_with_attrib]
            raise AttributeError(
                f"{conflicting_facilities} conflict for attribute '{name}'")
        else:
            facility = facilities_with_attrib[0]
            setattr(facility, name, value)

    def _managed_set_attrib(self, name, value):
        if name in self.__dict__:
            super().__setattr__(name, value)
        else:
            setattr(self._get_core(), name, value)

    def _facilities_with_attrib(self, name, called_from=None):
        facilities = []
        for facility, attribs in self._get_facilities():
            facility_name = facility.__class__.__name__
            if called_from == facility_name:
                break
            if name in attribs:
                facilities.append(facility_name)
        return facilities

    def __getattr__(self, name):
        facilities_with_attrib = self._facilities_with_attrib(name)
        if not facilities_with_attrib:
            return self._managed_get_attrib(name)
        last_facility = self._get_facility(facilities_with_attrib[-1])
        if len(facilities_with_attrib) == 1:
            return getattr(last_facility, name)
        if callable(getattr(last_facility, name)):
            raise AttributeError(
                f"Modular method needed for '{name}'?")
        conflicting_facilities = [
            type(facility).__name__ for facility in facilities_with_attrib]
        raise AttributeError(
            f"{conflicting_facilities} conflict for attribute '{name}'")

    def _managed_get_attrib(self, name):
        core = self._get_core()
        try:
            return getattr(core, name)
        except AttributeError:
            if name in core.__dict__:
                return core.__dict__[name]
        raise AttributeError(f"No attribute '{name}' found")

    def _set_attrib_value(self, name, value):
        self._get_attrib_values()[name] = value

    def _get_attrib_value(self, name):
        attrib_values = self._get_attrib_values()
        if name not in attrib_values:
            raise AttributeError(f"No attribute '{name}'")
        return attrib_values.get(name)

    def _del_attrib_value(self, name):
        attrib_values = self._get_attrib_values()
        if name not in attrib_values:
            raise AttributeError(f"No attribute '{name}' to delete")
        del attrib_values[name]

    def _stack_attrib_methods(self, method_name, called_from=None):
        facilities = self._facilities_with_attrib(method_name, called_from)
        self._get_method_stacks()[method_name] = facilities

    def _manage_attrib_method(self, method_name, *args, **kwargs):
        try:
            facility_name = self._get_method_stacks()[method_name].pop()
        except (KeyError, IndexError):
            return getattr(self._get_core(), method_name)(*args, **kwargs)
        facility = self._get_facility(facility_name)
        return getattr(facility, method_name)(*args, **kwargs)

    def _method_attrib_manager(self, method_name, called_from, *args, **kwargs):
        self._stack_attrib_methods(method_name, called_from)
        return self._manage_attrib_method(method_name, *args, **kwargs)
