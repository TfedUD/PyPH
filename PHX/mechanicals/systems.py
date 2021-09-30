# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Mechanical System Classes
"""

from collections import defaultdict
import PHX._base
import PHX.mechanicals.equipment
import PHX.mechanicals.distribution
import PHX.serialization.from_dict


class HVAC_System_Usage(PHX._base._Base):
    def __init__(self):
        super(HVAC_System_Usage, self).__init__()
        self.used_for_heating = False
        self.used_for_DHW = False
        self.used_for_cooling = False
        self.used_for_ventilation = False
        self.used_for_humidification = False
        self.used_for_dehumidification = False
        self.used_optional_climate = False
        self.optional_climate_id_number = -1


# ------------------------------------------------------------------------------
class Mechanicals(PHX._base._Base):
    """Container class to collect all the Mechanical Systems on the Room"""

    def __init__(self):
        super(Mechanicals, self).__init__()
        self._systems = defaultdict(list)

    def add_system(self, _system):
        self._systems[_system.identifier] = _system

    @property
    def systems(self):
        return self._systems.values()

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Mechanicals(cls, _dict)

    def __add__(self, _other):
        # type: (Mechanicals, Mechanicals) -> Mechanicals
        new_obj = self.__class__()
        new_obj._systems.update(self._systems)
        new_obj._systems.update(_other._systems)

        return new_obj

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


class MechanicalSystem(PHX._base._Base):
    """An individual Mechanical System (Vent, DHW, etc...) class"""

    _count = 0
    _default_ventilation = None

    def __init__(self):
        super(MechanicalSystem, self).__init__()
        self.id = self._count
        self.name = ""
        self.system_group_type_number = 1  # Ideal Air
        self.type_number = 1
        self.lZoneCover = []

        self.equipment_set = PHX.mechanicals.equipment.EquipmentSet()
        self.distribution = PHX.mechanicals.distribution.Distribution()
        self.system_usage = HVAC_System_Usage()

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(MechanicalSystem, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default_ventilation(cls):
        if cls._default_ventilation:
            return cls._default_ventilation

        new_obj = cls()
        new_obj.name = "Default Ventilation System"
        new_obj.type_number = 1
        new_obj.system_usage.used_for_ventilation = True

        cls._default_ventilation = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._MechanicalSystem(cls, _dict)
