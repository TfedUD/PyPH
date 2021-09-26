# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Program: Ventilation Classes
"""

import PHX._base
import PHX.programs.schedules
import PHX.programs.loads
import PHX.ventilation_components
import PHX.hvac
import PHX.serialization.from_dict


class SpaceVentilation(PHX._base._Base):

    _count = 0
    _default = None

    def __init__(self):
        super(SpaceVentilation, self).__init__()
        self.id = self._count
        self.name = ""
        self.loads = PHX.programs.loads.Load_Ventilation()
        self.schedule = PHX.programs.schedules.Schedule_Ventilation()
        self.system = PHX.ventilation_components.Ventilation_System()

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_space_ventialtion_"
        new_obj.schedule = PHX.programs.schedules.Schedule_Ventilation.default()
        new_obj.loads = PHX.programs.loads.Load_Ventilation.default()
        new_obj.system = PHX.ventilation_components.Ventilation_System.default()

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._SpaceVentilation(cls, _dict)

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(SpaceVentilation, cls).__new__(cls, *args, **kwargs)

    def __add__(self, _other):
        self.loads = self.loads.join(_other.loads)

        #
        #
        # TODO: Join Utilizations
        #
        #
        # TODO: Join Systems
        #
        #

        return self
