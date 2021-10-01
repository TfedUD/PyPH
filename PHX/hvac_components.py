# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Basic HVAC-Component Classes
"""

import PHX._base


class HVAC_Device(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(HVAC_Device, self).__init__()
        self.id = self._count
        self.Name = ""
        self.SystemType = None
        self.TypeDevice = None
        self.UsedFor_Heating = False
        self.UsedFor_DHW = False
        self.UsedFor_Cooling = False
        self.UsedFor_Ventilation = False
        self.UsedFor_Humidification = False
        self.UsedFor_Dehumidification = False
        self.UseOptionalClimate = False
        self.IdentNr_OptionalClimate = -1

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(HVAC_Device, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Device(cls, _dict)


class Ventilator_PH_Parameters(PHX._base._Base):
    def __init__(self):
        super(Ventilator_PH_Parameters, self).__init__()
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
        return PHX.serialization.from_dict._Ventilator_PH_Parameters(cls, _dict)


class HVAC_Ventilator(HVAC_Device):

    _count = 0
    _default = None

    def __init__(self):
        super(HVAC_Ventilator, self).__init__()
        self.id = self._count
        self.UsedFor_Ventilation = True
        self.PH_Parameters = Ventilator_PH_Parameters()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(HVAC_Device, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns a new Device for a default Ventilator (HRV/ERV)"""
        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.Name = "__default_ventilator__"
        new_obj.TypeDevice = 1
        new_obj.SystemType = 1

        cls._default = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Ventilator(cls, _dict)
