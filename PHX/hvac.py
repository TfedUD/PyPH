# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Basic HVAC Classes
"""

from ._base import _Base

class HVAC_PH_Parameters(_Base):
    
    def __init__(self):
        super(HVAC_PH_Parameters, self).__init__()
        self.HumidityRecoveryEfficiency = 0.0
        self.ElectricEfficiency = 0.45 #W/m3h
        self.FrostProtection = True
        self.Quantity = 1
        self.ElectricEfficiency = 0.45 #W/m3h
        self.SubsoilHeatExchangeEfficiency = 0.0
        self.HumidityRecoveryEfficiency = 0.0
        self.VolumeFlowRateFrom = None
        self.VolumeFlowRateTo = None
        self.TemperatureBelowDefrostUsed = None
        self.FrostProtection = True
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

class HVAC_Device(_Base):

    _count = 0

    def __init__(self):
        super(HVAC_Device, self).__init__()
        self.id = self._count
        self.Name = ''
        self.IdentNr = self.id
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
        """Used so I can keep a running tally for the id variable """
        
        cls._count += 1
        return super(HVAC_Device, cls).__new__(cls, *args, **kwargs)

class HVAC_System_ZoneCover(_Base):
    
    def __init__(self):
        super(HVAC_System_ZoneCover, self).__init__()
        self.idZone = 1
        self.czHCVHD = [1.0, 1.0, 1.0, 1.0, 1.0]

class HVAC_System(_Base):

    _count = 0

    def __init__(self):
        super(HVAC_System, self).__init__()
        self.n = ""
        self.typeSys = 1
        self.id = self._count
        self.lZoneCover = []
        self.lDevice = []
        self.distrib = None
        self.suppDev = None
        self.PHdistrib = None

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        
        cls._count += 1
        return super(HVAC_System, cls).__new__(cls, *args, **kwargs)

    def add_new_zone_hvac_system(self, _zone_hvac):
        # type: (HVAC_System_ZoneCover) -> None
        self.lZoneCover.append( _zone_hvac )
    
    def add_new_hvac_device(self, _hvac_device): 
        # type: (HVAC_Device) -> None
        self.lDevice.append( _hvac_device )


class HVAC(_Base):
    def __init__(self):
        super(HVAC, self).__init__()
        self.lSystem = []

    def add_system(self, _system):
        # type: (HVAC_System) -> None
        self.lSystem.append( _system )