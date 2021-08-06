# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Basic HVAC Classes
"""

from collections import defaultdict

import PHX._base
import PHX.serialization.from_dict
import PHX.variant


class HVAC_Ventilation_Airflows(PHX._base._Base):
    def __init__(self):
        super(HVAC_Ventilation_Airflows, self).__init__()
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
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Ventilation_Airflows(cls, _dict)

    def __repr__(self):
        return "{}(supply={:.02f}, extract={:.02f}, transfer={:.02f})".format(
            self.__class__.__name__, self.supply, self.extract, self.transfer
        )

    def __str__(self):
        return self.__repr__()


class HVAC_PH_Parameters(PHX._base._Base):
    def __init__(self):
        super(HVAC_PH_Parameters, self).__init__()
        self.HumidityRecoveryEfficiency = 0.0
        self.ElectricEfficiency = 0.45  # W/m3h
        self.FrostProtection = True
        self.Quantity = 1
        self.SubsoilHeatExchangeEfficiency = 0.0
        self.HumidityRecoveryEfficiency = 0.0
        self.VolumeFlowRateFrom = None
        self.VolumeFlowRateTo = None
        self.TemperatureBelowDefrostUsed = None
        self.DefrostRequired = False
        self.NoSummerBypass = True
        self.HRVCalculatorData = None
        self.Maximum_VOS = 0
        self.Maximum_PP = 100
        self.Standard_VOS = 0
        self.Standard_PP = 0
        self.Basic_VOS = 0
        self.Basic_PP = 0
        self.Minimum_VOS = 0
        self.Minimum_PP = 0
        self.AuxiliaryEnergy = None
        self.AuxiliaryEnergyDHW = None
        self.InConditionedSpace = True

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_PH_Parameters(cls, _dict)


class HVAC_Device(PHX._base._Base):

    _count = 0
    _default_ventilator = None

    def __init__(self):
        super(HVAC_Device, self).__init__()
        self.id = self._count
        self.Name = ""
        self.SystemType = None
        self.TypeDevice = None
        self.UsedFor_Heating = False
        self.UsedFor_DHW = False
        self.UsedFor_Cooling = False
        self.UsedFor_Ventilation = True
        self.UsedFor_Humidification = False
        self.UsedFor_Dehumidification = False
        self.Ventilation_Parameters = {}
        self.UseOptionalClimate = False
        self.IdentNr_OptionalClimate = -1
        self.PH_Parameters = HVAC_PH_Parameters()
        self.HeatRecovery = 0.75
        self.MoistureRecovery = 0.0

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(HVAC_Device, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default_ventilator(cls, *args, **kwargs):
        """Returns a new Device for a default Ventilator (HRV/ERV)"""
        if cls._default_ventilator:
            return cls._default_ventilator

        new_obj = cls()

        new_obj.Name = "__default_ventilation__"
        new_obj.TypeDevice = 1
        new_obj.SystemType = 1

        cls._default_ventilator = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Device(cls, _dict)


class HVAC_System_ZoneCover(PHX._base._Base):
    def __init__(self):
        super(HVAC_System_ZoneCover, self).__init__()
        self.idZoneCovered = 1
        self.cover_heating = 0
        self.cover_cooling = 0
        self.cover_ventilation = 0
        self.cover_humidification = 0
        self.cover_dehumidification = 0


class HVAC_System(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(HVAC_System, self).__init__()
        self.n = ""
        self.typeSys = 1
        self.id = self._count
        self.lZoneCover = []
        self._device_dict = defaultdict(list)
        self.distrib = None
        self.suppDev = None
        self.PHdistrib = None

    @property
    def lDevice(self):
        return list(self._device_dict.values())

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""

        cls._count += 1
        return super(HVAC_System, cls).__new__(cls, *args, **kwargs)

    def add_zone_to_system_coverage(self, _zone):
        # type: (HVAC_System_ZoneCover) -> None
        """Adds a Zone to the HVAC System's Covered Areas"""

        new_coverage = HVAC_System_ZoneCover()
        new_coverage.idZoneCovered = _zone.id

        self.lZoneCover.append(new_coverage)

    def add_zone_hvac_devices(self, _zones):
        # type: (list[PHX.variant.Zone]) -> None
        """Adds the HVAC Devices found on a Zone (Ventilation) to the HVAC System"""

        if not isinstance(_zones, list):
            _zones = [_zones]

        for zone in _zones:
            for space in zone.rooms_ventilation:
                self.add_devices_to_system(space.ventilation.ventilator)

    def add_devices_to_system(self, _devices):
        # type: (list[HVAC_Device]) -> None
        """Adds any HVAC Devices to the HVAC System"""

        if not isinstance(_devices, list):
            _devices = [_devices]

        # -- Ensure no duplicates
        for d in _devices:
            if not isinstance(d, HVAC_Device):
                raise Exception("Error")

            self._device_dict[d.id] = d


class HVAC(PHX._base._Base):
    def __init__(self):
        super(HVAC, self).__init__()
        self.lSystem = [HVAC_System()]

    @property
    def default_system(self):
        return self.lSystem[0]

    def add_system(self, _systems):
        # type: (HVAC_System) -> None
        if not isinstance(_systems, list):
            _systems = [_systems]

        for sys in _systems:
            self.lSystem.append(sys)
