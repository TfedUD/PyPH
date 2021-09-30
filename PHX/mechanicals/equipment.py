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
            * _devices (list[HVAC_Device])

        Returns:
        --------
            * None
        """

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


# ------------------------------------------------------------------------------
# -- HVAC
class HVAC_Device(PHX._base._Base):
    """Base Class for all HVAC Devices / Equipment"""

    _count = 0

    def __init__(self):
        super(HVAC_Device, self).__init__()
        self.id = self._count
        self.name = ""
        self.device_type = None

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(HVAC_Device, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Device(cls, _dict)


class HVAC_Ventilator_PH_Parameters(PHX._base._Base):
    def __init__(self):
        super(HVAC_Ventilator_PH_Parameters, self).__init__()
        self.ElectricEfficiency = 0.45  # W/m3h
        self.FrostProtection = True
        self.Quantity = 1
        self.SubsoilHeatExchangeEfficiency = 0.0
        self.HumidityRecoveryEfficiency = 0.0
        self.HeatRecoveryEfficiency = 0.75
        self.VolumeFlowRateFrom = 0.0
        self.VolumeFlowRateTo = 0.0
        self.TemperatureBelowDefrostUsed = -5  # C
        self.DefrostRequired = True
        self.NoSummerBypass = False
        self.HRVCalculatorData = None
        self.Maximum_VOS = 0
        self.Maximum_PP = 100
        self.Standard_VOS = 0
        self.Standard_PP = 0
        self.Basic_VOS = 0
        self.Basic_PP = 0
        self.Minimum_VOS = 0
        self.Minimum_PP = 0
        self.AuxiliaryEnergy = 0.0
        self.AuxiliaryEnergyDHW = 0.0
        self.InConditionedSpace = True

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Ventilator_PH_Parameters(cls, _dict)


class HVAC_Ventilator(HVAC_Device):

    _count = 0
    _default = None

    def __init__(self):
        super(HVAC_Ventilator, self).__init__()
        self.name = ""
        self.id = self._count
        self.device_type = 1
        self.PH_Parameters = HVAC_Ventilator_PH_Parameters()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(HVAC_Device, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns a new HVAC_Device for a default Ventilator (HRV/ERV)"""

        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.name = "__default_ventilator__"
        new_obj.device_type = 1

        cls._default = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Ventilator(cls, _dict)


# ------------------------------------------------------------------------------
# -- DHW
