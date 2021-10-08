# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Program: Load Classes
"""

import PHX._base
import PHX.serialization.from_dict


class Load_Lighting(PHX._base._Base):

    _default = None

    def __init__(self):
        super(Load_Lighting, self).__init__()
        self.name = ""
        self.target_lux = 0  # Lux
        self.target_lux_height = 0  # meters above floor
        self.watts_per_area = 0  # installed power density (W/m2)

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_load_lighting_"
        new_obj.target_lux = 300
        new_obj.target_lux_height = 0.8
        new_obj.watts_per_area = 10

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Load_Lighting(cls, _dict)

    @property
    def unique_key(self):
        return "{}_{}_{}_{}_".format(self.name, self.target_lux, self.target_lux_height, self.watts_per_area)


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

    def join(self, _other, _method="max"):
        # type: (Load_Ventilation, str) -> Load_Ventilation
        """Returns a new airflow object with the maximum values from each input

        Arguments:
        ----------
            * _other (PHX.progras.loads.Load_Ventilation): The other Load to Join with this one
            * _method (str) choose either:
                - 'max' (default): The largest flow-rate value from each object is used.
                - 'sum': The flow-rate values from both objects are summed together.

        Returns:
        --------
            * (PHX.programs.loads.Load_Ventilation): A new Load_Ventilation object with the new airfow rates.
        """
        if _other is None:
            return self

        new_obj = self.__class__()
        if _method.upper() == "MAX":
            new_obj.supply = max(self.supply, _other.supply)
            new_obj.extract = max(self.extract, _other.extract)
            new_obj.transfer = max(self.transfer, _other.transfer)
        elif _method.upper() == "SUM":
            new_obj.supply = self.supply + _other.supply
            new_obj.extract = self.extract + _other.extract
            new_obj.transfer = self.transfer + _other.transfer

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


class Load_ElecEquip(PHX._base._Base):

    _default = None

    def __init__(self):
        super(Load_ElecEquip, self).__init__()
        self.name = ""
        self.watts_per_area = 0  # installed power density (W/m2)

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_load_elec_equip_"
        new_obj.watts_per_area = 10

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Load_ElecEquip(cls, _dict)

    @property
    def unique_key(self):
        return "{}_{}_{}_".format(self.name, self.watts_per_area)
