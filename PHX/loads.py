# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Program Load Classes
"""

import PHX._base
import PHX.serialization.from_dict


class Load_Lighting(PHX._base._Base):

    _default = None

    def __init__(self):
        super(Load_Lighting, self).__init__()
        self.name = ""
        self.space_illumination = 0  # Lux
        self.installed_power_density = 0  # installed power density (W/m2)

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_load_lighting_"
        new_obj.space_illumination = 300
        new_obj.installed_power_density = 10

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Load_Lighting(cls, _dict)

    @property
    def unique_key(self):
        return "{}_{}_{}_".format(self.name, self.space_illumination, self.installed_power_density)


class Load_Occupancy(PHX._base._Base):

    _default = None

    def __init__(self):
        super(Load_Occupancy, self).__init__()
        self.name = ""
        self.people_per_area = 0  # ppl/m2

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_load_occupancy_"
        new_obj.people_per_area = 0.0565  # (HB Generic Office) = ~1 per/200ft2

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Load_Occupancy(cls, _dict)

    @property
    def unique_key(self):
        return "{}_{}_".format(self.name, self.people_per_area)


class Load_Ventilation(PHX._base._Base):

    _default = None

    def __init__(self):
        super(Load_Ventilation, self).__init__()
        self.name = ""
        self.supply = 0.0
        self.extract = 0.0
        self.transfer = 0.0

    def join(self, _other):
        """Returns a new airflow object with the maximum values from each input"""
        new_obj = self.__class__()

        new_obj.supply = max(self.supply, _other.supply)
        new_obj.extract = max(self.extract, _other.extract)
        new_obj.transfer = max(self.transfer, _other.transfer)

        return new_obj

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_load_ventilation_"
        new_obj.supply = 0.0
        new_obj.extract = 0.0
        new_obj.transfer = 0.0

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Load_Ventilation(cls, _dict)

    def __repr__(self):
        return "{}(supply={:.02f}, extract={:.02f}, transfer={:.02f})".format(
            self.__class__.__name__, self.supply, self.extract, self.transfer
        )

    def __str__(self):
        return self.__repr__()
