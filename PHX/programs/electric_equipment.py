# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Program: Electric Equipment Classes
"""

import PHX._base
import PHX.programs.schedules
import PHX.programs.loads
import PHX.serialization.from_dict


class RoomElectricEquipment(PHX._base._Base):

    _default = None

    def __init__(self):
        super(RoomElectricEquipment, self).__init__()
        self.name = ""
        self.schedule = PHX.programs.schedules.Schedule_ElecEquip()
        self.loads = PHX.programs.loads.Load_ElecEquip()

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_space_elec_equip_"
        new_obj.schedule = PHX.programs.schedules.Schedule_ElecEquip.default()
        new_obj.loads = PHX.programs.loads.Load_ElecEquip.default()

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._RoomElectricEquipment(cls, _dict)

    @property
    def unique_key(self):
        return "{}_{}_{}_".format(self.name, self.loads.unique_key, self.schedule.unique_key)
