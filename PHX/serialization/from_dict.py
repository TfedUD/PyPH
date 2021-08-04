# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
Functions for converting text dictionaries to PHX Objects. These functions are passed 
to the Object when it is instantiated in order to avoid circular reference problems since 
certain functions use other PHX Object to_dict() constructors.

ie: _Floor calls _FloorSegment.to_dict()
"""

import PHX
import PHX.geometry
import PHX.hvac
import PHX.spaces
import PHX.utilization_patterns
import LBT_Utils.geometry

#-- Utilization Patterns
def _VentilationUtilization(_cls, _input_dict):
    new_obj = _cls()

    new_obj.daily_op_sched = _input_dict.get('daily_op_sched')
    new_obj.frac_of_design_airflow = _input_dict.get('frac_of_design_airflow')

    return new_obj

def _VentilationUtilizations(_cls, _input_dict): # Collection
    new_obj = _cls()

    new_obj.maximum = PHX.utilization_patterns.VentilationUtilization.from_dict( _input_dict.get('maximum', {}) )
    new_obj.standard = PHX.utilization_patterns.VentilationUtilization.from_dict( _input_dict.get('standard', {}) )
    new_obj.basic = PHX.utilization_patterns.VentilationUtilization.from_dict( _input_dict.get('basic', {}) )
    new_obj.minimum = PHX.utilization_patterns.VentilationUtilization.from_dict( _input_dict.get('minimum', {}) )

    return new_obj

def _UtilizationPattern_Ventilation(_cls, _input_dict):
    new_obj = _cls()
    
    new_obj.id = _input_dict.get('id')
    new_obj.n = _input_dict.get('n' )
    new_obj.OperatingDays = _input_dict.get('OperatingDays')
    new_obj.OperatingWeeks = _input_dict.get('OperatingWeeks')

    new_obj.utilizations = PHX.utilization_patterns.VentilationUtilizations.from_dict( _input_dict.get('utilizations', {}) )
    
    return new_obj


#-- HVAC
def _PropertiesVentilation(_cls, _input_dict):
    new_obj = _cls()

    if _input_dict:
        new_obj.airflows = PHX.hvac.HVAC_Ventilation_Airflows.from_dict(_input_dict.get('airflows', {}))
        new_obj.ventilator = PHX.hvac.HVAC_Device.from_dict(_input_dict.get('ventilator', {}))
        new_obj.utilization_pattern = PHX.utilization_patterns.UtilizationPattern_Ventilation.from_dict(_input_dict.get('utilization_pattern', {}))

    return new_obj

def _HVAC_Ventilation_Airflows(_cls, _input_dict):
    new_obj = _cls()

    new_obj.supply = _input_dict.get('supply')
    new_obj.extract = _input_dict.get('extract')
    new_obj.transfer = _input_dict.get('transfer')

    return new_obj

def _HVAC_PH_Parameters(_cls, _input_dict):
    new_obj = _cls()

    new_obj.HumidityRecoveryEfficiency = _input_dict.get('HumidityRecoveryEfficiency')
    new_obj.ElectricEfficiency = _input_dict.get('ElectricEfficiency')
    new_obj.FrostProtection = _input_dict.get('FrostProtection')
    new_obj.Quantity = _input_dict.get('Quantity')
    new_obj.SubsoilHeatExchangeEfficiency = _input_dict.get('SubsoilHeatExchangeEfficiency')
    new_obj.HumidityRecoveryEfficiency = _input_dict.get('HumidityRecoveryEfficiency')
    new_obj.VolumeFlowRateFrom = _input_dict.get('VolumeFlowRateFrom')
    new_obj.VolumeFlowRateTo = _input_dict.get('VolumeFlowRateTo')
    new_obj.TemperatureBelowDefrostUsed = _input_dict.get('TemperatureBelowDefrostUsed')
    new_obj.DefrostRequired = _input_dict.get('DefrostRequired')
    new_obj.NoSummerBypass = _input_dict.get('NoSummerBypass')
    new_obj.HRVCalculatorData = _input_dict.get('HRVCalculatorData')
    new_obj.Maximum_VOS = _input_dict.get('Maximum_VOS')
    new_obj.Maximum_PP = _input_dict.get('Maximum_PP')
    new_obj.Standard_VOS = _input_dict.get('Standard_VOS')
    new_obj.Standard_PP = _input_dict.get('Standard_PP')
    new_obj.Basic_VOS = _input_dict.get('Basic_VOS')
    new_obj.Basic_PP = _input_dict.get('Basic_PP')
    new_obj.Minimum_VOS = _input_dict.get('Minimum_VOS')
    new_obj.Minimum_PP = _input_dict.get('Minimum_PP')
    new_obj.AuxiliaryEnergy = _input_dict.get('AuxiliaryEnergy')
    new_obj.AuxiliaryEnergyDHW = _input_dict.get('AuxiliaryEnergyDHW')
    new_obj.InConditionedSpace = _input_dict.get('InConditionedSpace')

    return new_obj

def _HVAC_Device(_cls, _input_dict):
    new_obj = _cls()

    new_obj.id = _input_dict.get('id')
    new_obj.Name = _input_dict.get('Name')
    new_obj.SystemType = _input_dict.get('SystemType')
    new_obj.TypeDevice = _input_dict.get('TypeDevice')
    new_obj.UsedFor_Heating = _input_dict.get('UsedFor_Heating')
    new_obj.UsedFor_DHW = _input_dict.get('UsedFor_DHW')
    new_obj.UsedFor_Cooling = _input_dict.get('UsedFor_Cooling')
    new_obj.UsedFor_Ventilation = _input_dict.get('UsedFor_Ventilation')
    new_obj.UsedFor_Humidification = _input_dict.get('UsedFor_Humidification')
    new_obj.UsedFor_Dehumidification = _input_dict.get('UsedFor_Dehumidification')
    new_obj.Ventilation_Parameters = _input_dict.get('Ventilation_Parameters')
    new_obj.UseOptionalClimate = _input_dict.get('UseOptionalClimate')
    new_obj.IdentNr_OptionalClimate = _input_dict.get('IdentNr_OptionalClimate')
    new_obj.PH_Parameters = PHX.hvac.HVAC_PH_Parameters.from_dict(_input_dict.get('PH_Parameters.to_dict()', {}))
    new_obj.HeatRecovery = _input_dict.get('HeatRecovery')
    new_obj.MoistureRecovery = _input_dict.get('MoistureRecovery')

    return new_obj


#-- Spaces
def _FloorSegment(_cls, _input_dict):
    new_obj = _cls()

    new_obj.weighting_factor = _input_dict.get('weighting_factor')
    new_obj.floor_area_gross = _input_dict.get('floor_area_gross')
    new_obj.space_name = _input_dict.get('space_name')
    new_obj.space_number = _input_dict.get('space_number')
    new_obj.non_res_lighting = _input_dict.get('non_res_lighting')
    new_obj.non_res_motion = _input_dict.get('non_res_motion')
    new_obj.non_res_usage = _input_dict.get('non_res_usage')
    new_obj.ventilation_v_sup = _input_dict.get('ventilation_v_sup')
    new_obj.ventilation_v_eta = _input_dict.get('ventilation_v_eta')
    new_obj.ventilation_v_trans = _input_dict.get('ventilation_v_trans')
    new_obj.host_zone_identifier = _input_dict.get('host_zone_identifier')

    for _ in _input_dict.get('geometry', {}).values():
        new_obj.geometry.append(LBT_Utils.geometry.LBT_geometry_dict_util(_))

    return new_obj

def _Floor(_cls, _input_dict):
    new_obj = _cls()
        
    new_obj.space_name = _input_dict.get('space_name')
    new_obj.space_number = _input_dict.get('space_number')
    new_obj.non_res_lighting = _input_dict.get('non_res_lighting')
    new_obj.non_res_motion = _input_dict.get('non_res_motion')
    new_obj.non_res_usage = _input_dict.get('non_res_usage')
    new_obj.ventilation_v_sup = _input_dict.get('ventilation_v_sup')
    new_obj.ventilation_v_eta = _input_dict.get('ventilation_v_eta')
    new_obj.ventilation_v_trans = _input_dict.get('ventilation_v_trans')
    new_obj.host_zone_identifier = _input_dict.get('host_zone_identifier')

    new_obj.floor_segments = []
    for flr_seg_dict in _input_dict.get('floor_segments', {}).values():
        if flr_seg_dict:
            new_flr_seg = PHX.spaces.FloorSegment.from_dict(flr_seg_dict)
            new_obj.floor_segments.append( new_flr_seg )

    return new_obj

def _Volume(_cls, _input_dict):
    new_obj = _cls()

    new_obj.space_name = _input_dict.get('space_name')
    new_obj.space_number = _input_dict.get('space_number')
    new_obj.host_zone_identifier = _input_dict.get('host_zone_identifier')
    new_obj._average_ceiling_height = _input_dict.get('_average_ceiling_height')
    new_obj._volume = _input_dict.get('_volume')
    
    floor_dict = _input_dict.get('floor')
    if floor_dict:
        new_obj.floor = PHX.spaces.Floor.from_dict(floor_dict)

    new_obj.volume_geometry= []
    for _ in _input_dict.get('volume_geometry', {}).values():
        new_geom_list = []
        for __ in _.values():
            new_geom_list.append( LBT_Utils.geometry.LBT_geometry_dict_util(__) )
        new_obj.volume_geometry.append(new_geom_list)

    return new_obj

def _Space(_cls, _input_dict):
    new_obj = _cls()

    new_obj.space_name = _input_dict.get('space_name')
    new_obj.space_number = _input_dict.get('space_number')
    new_obj.host_zone_identifier = _input_dict.get('host_zone_identifier')
    new_obj.occupancy = _input_dict.get('occupancy')
    new_obj.equipment = _input_dict.get('equipment')
    new_obj.ventilation = PHX.spaces.PropertiesVentilation.from_dict( _input_dict.get('ventilation', {}) )

    new_obj.volumes = []
    for volume_dict in _input_dict.get('volumes', {}).values():
        new_obj.volumes.append( PHX.spaces.Volume.from_dict(volume_dict) )

    return new_obj