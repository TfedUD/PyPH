# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Mechanical Equipment Classes
"""

import PHX._base
import PHX.serialization.from_dict

# ------------------------------------------------------------------------------
class EquipmentSet(PHX._base._Base):
    """Container class for Mechancial Equipment of any sort"""

    _count = 0

    def __init__(self):
        super(EquipmentSet, self).__init__()
        self.id = self._count
        self._equipment = {}

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(EquipmentSet, cls).__new__(cls, *args, **kwargs)

    @property
    def equipment(self):
        return self._equipment.values()

    def add_new_device_to_equipment_set(self, _devices):
        # type: (HVAC_Device) -> None
        """Adds a Device to the set. Will disregard duplicates.

        Arguments:
        ----------
            * _devices (list[HVAC_Device] | None)

        Returns:
        --------
            * None
        """

        if not _devices:
            return

        if not isinstance(_devices, list):
            _devices = [_devices]

        for device in _devices:
            self._equipment[device.identifier] = device

    def get_all_devices_by_type(self, _type_number=1):
        # type: (int) -> list[HVAC_Device]
        """Returns a list of all the devices in the EquipmentSet with the designated type number.

        Arguments:
        ----------
            * _type_number (int): The type-number to search for.

        Returns:
        --------
            * (list): A list of equipment of the specified type.
        """

        return [d for d in self.equipment if d.device_type == _type_number]

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._EquipmentSet(cls, _dict)


class HVAC_Device_Properties(PHX._base._Base):
    """A super simple class to hold onto property data"""

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Device_Properties(cls, _dict)


# ------------------------------------------------------------------------------
# -- HVAC
class HVAC_Device(PHX._base._Base):
    """Base Class for all HVAC Devices / Equipment"""

    _default_properties = {}

    def __init__(self):
        super(HVAC_Device, self).__init__()
        self.name = ""
        self.id = None
        self.device_type = None
        self.system_type = None
        self.properties = HVAC_Device_Properties()

    def __new__(cls, *args, **kwargs):
        """
        Developer Note: _count and .id is NOT implemented in this base class but should be implemented
        by all sublcasses directly instead. Otherwise you will end up with funny results.
        """
        return super(HVAC_Device, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Device(cls, _dict)


class HVAC_Ventilator(HVAC_Device):

    _count = 0
    _default = None
    _default_properties = {
        "electric_efficiency": {"base": 0, "default": 0.45},
        "frost_protection": {"base": True, "default": 0},
        "quantity": {"base": 1, "default": 0},
        "subsoil_heat_exchange_efficiency": {"base": 0, "default": 0},
        "humidity_recovery_efficiency": {"base": 0, "default": 0},
        "heat_recovery_efficiency": {"base": 0, "default": 0.75},
        "volume_flowrate_from": {"base": 0, "default": 0},
        "volume_flow_rate_to": {"base": 0, "default": 0},
        "temperature_below_defrost_used": {"base": 0, "default": -5},
        "defrost_required": {"base": False, "default": 0},
        "no_summer_bypass": {"base": False, "default": 0},
        "hrv_calculator_data": {"base": None, "default": 0},
        "maximum_vos": {"base": 0, "default": 0},
        "maximum_pp": {"base": 100, "default": 0},
        "standard_vos": {"base": 0, "default": 0},
        "standard_pp": {"base": 0, "default": 0},
        "basic_vos": {"base": 0, "default": 0},
        "basic_pp": {"base": 0, "default": 0},
        "minimum_vos": {"base": 0, "default": 0},
        "minimum_pp": {"base": 0, "default": 0},
        "auxiliary_energy": {"base": 0, "default": 0},
        "auxiliary_energy_dhw": {"base": 0, "default": 0},
        "in_conditioned_space": {"base": True, "default": 0},
    }

    def __init__(self):
        super(HVAC_Ventilator, self).__init__()
        self.name = ""
        self.id = self._count
        self.device_type = 1
        self.system_type = 1
        self.properties = HVAC_Device_Properties()
        self._set_property_fields("base")

    def _set_property_fields(self, _type="base"):
        for k, v in self._default_properties.items():
            setattr(self.properties, k, v.get(_type))

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(HVAC_Ventilator, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns a new HVAC_Device for a default Ventilator (HRV/ERV)"""

        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.name = "__default_ventilator__"
        new_obj.device_type = 1
        new_obj.system_type = 1

        # -- Set default properties
        new_obj._set_property_fields("default")

        cls._default = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Ventilator(cls, _dict)


# ------------------------------------------------------------------------------
# -- DHW
class HW_Tank(HVAC_Device):

    _count = 0
    _default = None
    _default_properties = {
        "quantity": {"base": 1, "default": 1},
        "volume": {"base": 0, "default": 300},  # 300L == 80 Gallon
        "standby_loses": {"base": 0, "default": 4},
    }

    def __init__(self):
        super(HW_Tank, self).__init__()
        self.name = ""
        self.id = self._count
        self.device_type = 8  # water storage
        self.system_type = 8
        self.properties = HVAC_Device_Properties()
        self._set_property_fields("base")

    def _set_property_fields(self, _type="base"):
        for k, v in self._default_properties.items():
            setattr(self.properties, k, v.get(_type))

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(HW_Tank, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns a new HVAC_Device for a default HW Tank"""

        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.name = "__default_HW_tank__"
        new_obj.device_type = 8  # Water storage
        new_obj.system_type = 8

        # -- Set default properties
        new_obj._set_property_fields("default")

        cls._default = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HW_Tank(cls, _dict)


class HW_Heater_Direct_Elec(HVAC_Device):
    _count = 0
    _default = None
    _default_properties = {
        "watts": {"base": 0, "default": 2000},
    }

    def __init__(self):
        super(HW_Heater_Direct_Elec, self).__init__()
        self.name = ""
        self.id = self._count
        self.device_type = 2  # Electric resistance space heat / DHW
        self.system_type = 2
        self.properties = HVAC_Device_Properties()
        self._set_property_fields("base")

    def _set_property_fields(self, _type="base"):
        for k, v in self._default_properties.items():
            setattr(self.properties, k, v.get(_type))

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(HW_Heater_Direct_Elec, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns a new HVAC_Device for a default HW Direct Electtric Heater"""

        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.name = "__default_HW_tank__"
        new_obj.device_type = 2  # Electric resistance space heat / DHW
        new_obj.system_type = 2

        new_obj._set_property_fields("default")

        cls._default = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HW_Heater_Direct_Elec(cls, _dict)

    def __str__(self):
        return "PHX_{}(name={!r}, device_type={!r})".format(self.__class__.__name__, self.name, self.device_type)
