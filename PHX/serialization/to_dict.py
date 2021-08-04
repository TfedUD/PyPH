# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
Functions for converting PHX Objects to serializable text dictionaries. All PHX Objects
should be able to be converted to fully text represenations.
"""

#-- Utilization Patterns
def _VentilationUtilization(_obj):
    d = {}

    d.update( { 'daily_op_sched': _obj.daily_op_sched }  )
    d.update( { 'frac_of_design_airflow': _obj.frac_of_design_airflow }  )

    return d

def _VentilationUtilizations(_obj): # Collection
    d = {}

    d.update( { 'maximum': _obj.maximum.to_dict() }  )
    d.update( { 'standard': _obj.standard.to_dict() }  )
    d.update( { 'basic': _obj.basic.to_dict() }  )
    d.update( { 'minimum': _obj.minimum.to_dict() }  )

    return d

def _UtilizationPattern_Ventilation(_obj):
    d = {}
    
    d.update( { 'id': _obj.id}  )
    d.update( { 'n': _obj.n}  )
    d.update( { 'OperatingDays': _obj.OperatingDays}  )
    d.update( { 'OperatingWeeks': _obj.OperatingWeeks }  )

    d.update( { 'utilizations': _obj.utilizations.to_dict() }  )
    
    return d


#-- HVAC
def _PropertiesVentilation(_obj):
    d = {}

    d.update( { 'airflows': _obj.airflows.to_dict() }  )
    d.update( { 'ventilator': _obj.ventilator.to_dict() }  )
    d.update( { 'utilization_pattern': _obj.utilization_pattern.to_dict() }  )

    return d

def _HVAC_Ventilation_Airflows(_obj):
    d = {}

    d.update( { 'supply': _obj.supply }  )
    d.update( { 'extract': _obj.extract }  )
    d.update( { 'transfer': _obj.transfer }  )

    return d

def _HVAC_PH_Parameters(_obj):
    d = {}

    d.update( { 'HumidityRecoveryEfficiency': _obj.HumidityRecoveryEfficiency }  )
    d.update( { 'ElectricEfficiency': _obj.ElectricEfficiency }  )
    d.update( { 'FrostProtection': _obj.FrostProtection }  )
    d.update( { 'Quantity': _obj.Quantity }  )
    d.update( { 'SubsoilHeatExchangeEfficiency': _obj.SubsoilHeatExchangeEfficiency }  )
    d.update( { 'HumidityRecoveryEfficiency': _obj.HumidityRecoveryEfficiency }  )
    d.update( { 'VolumeFlowRateFrom': _obj.VolumeFlowRateFrom }  )
    d.update( { 'VolumeFlowRateTo': _obj.VolumeFlowRateTo }  )
    d.update( { 'TemperatureBelowDefrostUsed': _obj.TemperatureBelowDefrostUsed }  )
    d.update( { 'DefrostRequired': _obj.DefrostRequired }  )
    d.update( { 'NoSummerBypass': _obj.NoSummerBypass }  )
    d.update( { 'HRVCalculatorData': _obj.HRVCalculatorData }  )
    d.update( { 'Maximum_VOS': _obj.Maximum_VOS }  )
    d.update( { 'Maximum_PP': _obj.Maximum_PP }  )
    d.update( { 'Standard_VOS': _obj.Standard_VOS }  )
    d.update( { 'Standard_PP': _obj.Standard_PP }  )
    d.update( { 'Basic_VOS': _obj.Basic_VOS }  )
    d.update( { 'Basic_PP': _obj.Basic_PP }  )
    d.update( { 'Minimum_VOS': _obj.Minimum_VOS }  )
    d.update( { 'Minimum_PP': _obj.Minimum_PP }  )
    d.update( { 'AuxiliaryEnergy': _obj.AuxiliaryEnergy }  )
    d.update( { 'AuxiliaryEnergyDHW': _obj.AuxiliaryEnergyDHW }  )
    d.update( { 'InConditionedSpace': _obj.InConditionedSpace }  )

    return d

def _HVAC_Device(_obj):
    d = {}

    d.update( { 'id': _obj.id }  )
    d.update( { 'Name': _obj.Name }  )
    d.update( { 'SystemType': _obj.SystemType }  )
    d.update( { 'TypeDevice': _obj.TypeDevice }  )
    d.update( { 'UsedFor_Heating': _obj.UsedFor_Heating }  )
    d.update( { 'UsedFor_DHW': _obj.UsedFor_DHW }  )
    d.update( { 'UsedFor_Cooling': _obj.UsedFor_Cooling }  )
    d.update( { 'UsedFor_Ventilation': _obj.UsedFor_Ventilation }  )
    d.update( { 'UsedFor_Humidification': _obj.UsedFor_Humidification }  )
    d.update( { 'UsedFor_Dehumidification': _obj.UsedFor_Dehumidification }  )
    d.update( { 'Ventilation_Parameters': _obj.Ventilation_Parameters }  )
    d.update( { 'UseOptionalClimate': _obj.UseOptionalClimate }  )
    d.update( { 'IdentNr_OptionalClimate': _obj.IdentNr_OptionalClimate }  )
    d.update( { 'PH_Parameters': _obj.PH_Parameters.to_dict() }  )
    d.update( { 'HeatRecovery': _obj.HeatRecovery }  )
    d.update( { 'MoistureRecovery': _obj.MoistureRecovery }  )

    return d


#-- Spaces
def _FloorSegment(_obj):
    d = {}  

    d.update( { 'weighting_factor': _obj.weighting_factor }  )
    d.update( { 'floor_area_gross': _obj.floor_area_gross }  )
    d.update( { 'space_name': _obj.space_name }  )
    d.update( { 'space_number': _obj.space_number }  )
    d.update( { 'non_res_lighting': _obj.non_res_lighting }  )
    d.update( { 'non_res_motion': _obj.non_res_motion }  )
    d.update( { 'non_res_usage': _obj.non_res_usage }  )
    d.update( { 'ventilation_v_sup': _obj.ventilation_v_sup }  )
    d.update( { 'ventilation_v_eta': _obj.ventilation_v_eta }  )
    d.update( { 'ventilation_v_trans': _obj.ventilation_v_trans }  )
    d.update( { 'host_zone_identifier': _obj.host_zone_identifier }  )
    
    geometry_dict = {}
    for _ in _obj.geometry:
        geometry_dict.update( { id(_): _.to_dict() } )
    d.update( { 'geometry': geometry_dict }  )

    return d 

def _Floor(_obj):
    d = {}

    d.update( { 'space_name': _obj.space_name }  )
    d.update( { 'space_number': _obj.space_number }  )
    d.update( { 'non_res_lighting': _obj.non_res_lighting }  )
    d.update( { 'non_res_motion': _obj.non_res_motion }  )
    d.update( { 'non_res_usage': _obj.non_res_usage }  )
    d.update( { 'ventilation_v_sup': _obj.ventilation_v_sup }  )
    d.update( { 'ventilation_v_eta': _obj.ventilation_v_eta }  )
    d.update( { 'ventilation_v_trans': _obj.ventilation_v_trans }  )
    d.update( { 'host_zone_identifier': _obj.host_zone_identifier }  )

    floor_segments_dict = {}
    for flr_seg in _obj.floor_segments:
        floor_segments_dict.update( { id(flr_seg): flr_seg.to_dict() } )
    d.update( { 'floor_segments': floor_segments_dict }  )

    return d

def _Volume(_obj):
    d = {}

    d.update( { 'space_name': _obj.space_name }  )
    d.update( { 'space_number': _obj.space_number }  )
    d.update( { 'host_zone_identifier': _obj.host_zone_identifier }  )
    d.update( { '_average_ceiling_height': _obj._average_ceiling_height }  )
    d.update( { '_volume': _obj._volume }  )
    
    d.update( { 'floor': _obj.floor.to_dict() }  )

    volume_geometry_dict = {}
    for list_of_geom in _obj.volume_geometry:
        geom_list = {}
        for geom in list_of_geom:
            geom_list.update( { id(geom): geom.to_dict() } )
        volume_geometry_dict.update( { id(geom_list):geom_list } )

    d.update( { 'volume_geometry': volume_geometry_dict }  )

    return d

def _Space(_obj):
    d = {}

    d.update( { 'space_name': _obj.space_name }  )
    d.update( { 'space_number': _obj.space_number }  )
    d.update( { 'host_zone_identifier': _obj.host_zone_identifier }  )
    d.update( { 'occupancy': _obj.occupancy }  )
    d.update( { 'equipment': _obj.equipment }  )
    d.update( { 'ventilation': _obj.ventilation.to_dict() }  )

    volumes_dict = {}
    for volume in _obj.volumes:
        volumes_dict.update( { id(volume):volume.to_dict() } )
    d.update( { 'volumes': volumes_dict }  )

    return d