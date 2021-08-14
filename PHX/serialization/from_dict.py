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

# -- Utilization Patterns
def _VentilationUtilization(_cls, _input_dict):
    new_obj = _cls()

    new_obj.daily_op_sched = _input_dict.get("daily_op_sched")
    new_obj.frac_of_design_airflow = _input_dict.get("frac_of_design_airflow")

    return new_obj


def _VentilationUtilizations(_cls, _input_dict):  # Collection
    new_obj = _cls()

    new_obj.maximum = PHX.utilization_patterns.VentilationUtilization.from_dict(_input_dict.get("maximum", {}))
    new_obj.standard = PHX.utilization_patterns.VentilationUtilization.from_dict(_input_dict.get("standard", {}))
    new_obj.basic = PHX.utilization_patterns.VentilationUtilization.from_dict(_input_dict.get("basic", {}))
    new_obj.minimum = PHX.utilization_patterns.VentilationUtilization.from_dict(_input_dict.get("minimum", {}))

    return new_obj


def _UtilizationPattern_Ventilation(_cls, _input_dict):
    new_obj = _cls()

    new_obj.id = _input_dict.get("id")
    new_obj.n = _input_dict.get("n")
    new_obj.OperatingDays = _input_dict.get("OperatingDays")
    new_obj.OperatingWeeks = _input_dict.get("OperatingWeeks")

    new_obj.utilizations = PHX.utilization_patterns.VentilationUtilizations.from_dict(
        _input_dict.get("utilizations", {})
    )

    return new_obj


# -- Ventilation
def _SummerVent(_cls, _input_dict):
    new_obj = _cls()

    new_obj.avg_mech_ach = _input_dict.get("avg_mech_ach")
    new_obj.day_window_ach = _input_dict.get("day_window_ach")
    new_obj.night_window_ach = _input_dict.get("night_window_ach")
    new_obj.additional_mech_ach = _input_dict.get("additional_mech_ach")
    new_obj.additional_mech_spec_power = _input_dict.get("additional_mech_spec_power")
    new_obj.exhaust_ach = _input_dict.get("exhaust_ach")
    new_obj.exhaust_spec_power = _input_dict.get("exhaust_spec_power")
    new_obj.additional_mech_control_mode = _input_dict.get("additional_mech_control_mode")
    new_obj.avg_mech_control_mode = _input_dict.get("avg_mech_control_mode")

    return new_obj


# -- HVAC: Ventilation
def _HVAC_Ventilation_Duct_Segment(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.length = _input_dict.get("length")
    new_obj.diameter = _input_dict.get("diameter")
    new_obj.width = _input_dict.get("width")
    new_obj.height = _input_dict.get("height")
    new_obj.insulation_thickness = _input_dict.get("insulation_thickness")
    new_obj.insulation_conductivity = _input_dict.get("insulation_conductivity")

    return new_obj


def _HVAC_Ventilation_Duct(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    for d in _input_dict.get("segments"):
        new_obj.segments.append(PHX.hvac.HVAC_Ventilation_Duct_Segment.from_dict(d))

    return new_obj


def _HVAC_Ventilation_System(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.type = _input_dict.get("type")

    new_obj.duct_01 = PHX.hvac.HVAC_Device.from_dict(_input_dict.get("ventilator", {}))
    new_obj.duct_01 = PHX.hvac.HVAC_Ventilation_Duct.from_dict(_input_dict.get("duct_01", {}))
    new_obj.duct_02 = PHX.hvac.HVAC_Ventilation_Duct.from_dict(_input_dict.get("duct_02", {}))

    return new_obj


# -- HVAC
def _PropertiesVentilation(_cls, _input_dict):
    new_obj = _cls()

    if _input_dict:
        new_obj.airflows = PHX.hvac.HVAC_Ventilation_Airflows.from_dict(_input_dict.get("airflows", {}))
        new_obj.ventilator = PHX.hvac.HVAC_Device.from_dict(_input_dict.get("ventilator", {}))
        new_obj.utilization_pattern = PHX.utilization_patterns.UtilizationPattern_Ventilation.from_dict(
            _input_dict.get("utilization_pattern", {})
        )

    return new_obj


def _HVAC_Ventilation_Airflows(_cls, _input_dict):
    new_obj = _cls()

    new_obj.supply = _input_dict.get("supply")
    new_obj.extract = _input_dict.get("extract")
    new_obj.transfer = _input_dict.get("transfer")

    return new_obj


def _HVAC_PH_Parameters(_cls, _input_dict):
    new_obj = _cls()

    new_obj.HumidityRecoveryEfficiency = _input_dict.get("HumidityRecoveryEfficiency")
    new_obj.ElectricEfficiency = _input_dict.get("ElectricEfficiency")
    new_obj.FrostProtection = _input_dict.get("FrostProtection")
    new_obj.Quantity = _input_dict.get("Quantity")
    new_obj.SubsoilHeatExchangeEfficiency = _input_dict.get("SubsoilHeatExchangeEfficiency")
    new_obj.HumidityRecoveryEfficiency = _input_dict.get("HumidityRecoveryEfficiency")
    new_obj.VolumeFlowRateFrom = _input_dict.get("VolumeFlowRateFrom")
    new_obj.VolumeFlowRateTo = _input_dict.get("VolumeFlowRateTo")
    new_obj.TemperatureBelowDefrostUsed = _input_dict.get("TemperatureBelowDefrostUsed")
    new_obj.DefrostRequired = _input_dict.get("DefrostRequired")
    new_obj.NoSummerBypass = _input_dict.get("NoSummerBypass")
    new_obj.HRVCalculatorData = _input_dict.get("HRVCalculatorData")
    new_obj.Maximum_VOS = _input_dict.get("Maximum_VOS")
    new_obj.Maximum_PP = _input_dict.get("Maximum_PP")
    new_obj.Standard_VOS = _input_dict.get("Standard_VOS")
    new_obj.Standard_PP = _input_dict.get("Standard_PP")
    new_obj.Basic_VOS = _input_dict.get("Basic_VOS")
    new_obj.Basic_PP = _input_dict.get("Basic_PP")
    new_obj.Minimum_VOS = _input_dict.get("Minimum_VOS")
    new_obj.Minimum_PP = _input_dict.get("Minimum_PP")
    new_obj.AuxiliaryEnergy = _input_dict.get("AuxiliaryEnergy")
    new_obj.AuxiliaryEnergyDHW = _input_dict.get("AuxiliaryEnergyDHW")
    new_obj.InConditionedSpace = _input_dict.get("InConditionedSpace")

    return new_obj


def _HVAC_Device(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.Name = _input_dict.get("Name")
    new_obj.SystemType = _input_dict.get("SystemType")
    new_obj.TypeDevice = _input_dict.get("TypeDevice")
    new_obj.UsedFor_Heating = _input_dict.get("UsedFor_Heating")
    new_obj.UsedFor_DHW = _input_dict.get("UsedFor_DHW")
    new_obj.UsedFor_Cooling = _input_dict.get("UsedFor_Cooling")
    new_obj.UsedFor_Ventilation = _input_dict.get("UsedFor_Ventilation")
    new_obj.UsedFor_Humidification = _input_dict.get("UsedFor_Humidification")
    new_obj.UsedFor_Dehumidification = _input_dict.get("UsedFor_Dehumidification")
    new_obj.Ventilation_Parameters = _input_dict.get("Ventilation_Parameters")
    new_obj.UseOptionalClimate = _input_dict.get("UseOptionalClimate")
    new_obj.IdentNr_OptionalClimate = _input_dict.get("IdentNr_OptionalClimate")
    new_obj.PH_Parameters = PHX.hvac.HVAC_PH_Parameters.from_dict(_input_dict.get("PH_Parameters", {}))

    return new_obj


def _HVAC_System(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.n = _input_dict.get("n")
    new_obj.typeSys = _input_dict.get("typeSys")
    new_obj.lZoneCover = _input_dict.get("lZoneCover")
    new_obj._device_dict = _input_dict.get("_device_dict")
    new_obj.distrib = _input_dict.get("distrib")
    new_obj.suppDev = _input_dict.get("suppDev")
    new_obj.PHdistrib = _input_dict.get("PHdistrib")

    return new_obj


# -- Spaces
def _FloorSegment(_cls, _input_dict):
    new_obj = _cls()

    new_obj.weighting_factor = _input_dict.get("weighting_factor")
    new_obj.floor_area_gross = _input_dict.get("floor_area_gross")
    new_obj.space_name = _input_dict.get("space_name")
    new_obj.space_number = _input_dict.get("space_number")
    new_obj.non_res_lighting = _input_dict.get("non_res_lighting")
    new_obj.non_res_motion = _input_dict.get("non_res_motion")
    new_obj.non_res_usage = _input_dict.get("non_res_usage")
    new_obj._ventilation = PHX.spaces.PropertiesVentilation.from_dict(_input_dict.get("_ventilation", {}))
    new_obj.host_zone_identifier = _input_dict.get("host_zone_identifier")

    for _ in _input_dict.get("geometry", {}).values():
        new_obj.geometry.append(LBT_Utils.geometry.LBT_geometry_dict_util(_))

    return new_obj


def _Floor(_cls, _input_dict):
    new_obj = _cls()

    new_obj.space_name = _input_dict.get("space_name")
    new_obj.space_number = _input_dict.get("space_number")
    new_obj.non_res_lighting = _input_dict.get("non_res_lighting")
    new_obj.non_res_motion = _input_dict.get("non_res_motion")
    new_obj.non_res_usage = _input_dict.get("non_res_usage")
    new_obj._ventilation = PHX.spaces.PropertiesVentilation.from_dict(_input_dict.get("_ventilation", {}))
    new_obj.host_zone_identifier = _input_dict.get("host_zone_identifier")

    new_obj.floor_segments = []
    for flr_seg_dict in _input_dict.get("floor_segments", {}).values():
        if flr_seg_dict:
            new_flr_seg = PHX.spaces.FloorSegment.from_dict(flr_seg_dict)
            new_obj.floor_segments.append(new_flr_seg)

    return new_obj


def _Volume(_cls, _input_dict):
    new_obj = _cls()

    new_obj.space_name = _input_dict.get("space_name")
    new_obj.space_number = _input_dict.get("space_number")
    new_obj.host_zone_identifier = _input_dict.get("host_zone_identifier")
    new_obj._average_ceiling_height = _input_dict.get("_average_ceiling_height")
    new_obj._volume = _input_dict.get("_volume")

    floor_dict = _input_dict.get("floor")
    if floor_dict:
        new_obj.floor = PHX.spaces.Floor.from_dict(floor_dict)

    new_obj.volume_geometry = []
    for _ in _input_dict.get("volume_geometry", {}).values():
        new_geom_list = []
        for __ in _.values():
            new_geom_list.append(LBT_Utils.geometry.LBT_geometry_dict_util(__))
        new_obj.volume_geometry.append(new_geom_list)

    new_obj._ventilation = PHX.spaces.PropertiesVentilation.from_dict(_input_dict.get("_ventilation", {}))

    return new_obj


def _Space(_cls, _input_dict):
    new_obj = _cls()

    new_obj.space_name = _input_dict.get("space_name")
    new_obj.space_number = _input_dict.get("space_number")
    new_obj.host_zone_identifier = _input_dict.get("host_zone_identifier")
    new_obj.occupancy = _input_dict.get("occupancy")
    new_obj.equipment = _input_dict.get("equipment")
    new_obj.ventilation = PHX.spaces.PropertiesVentilation.from_dict(_input_dict.get("ventilation", {}))
    new_obj.volume = _input_dict.get("volume")  # Number
    new_obj.volumes = []  # Volume Objects
    for volume_dict in _input_dict.get("volumes", {}).values():
        new_obj.volumes.append(PHX.spaces.Volume.from_dict(volume_dict))

    return new_obj


# -- Occupany
def _BldgSegmentOccupancy(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.category = _input_dict.get("category")
    new_obj.usage_type = _input_dict.get("usage_type")
    new_obj.num_units = _input_dict.get("num_units")
    new_obj.num_stories = _input_dict.get("num_stories")

    return new_obj


# -- Passive House Certification
def _PHIUSCertification(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.certification_criteria = _input_dict.get("certification_criteria")
    new_obj.localization_selection_type = _input_dict.get("localization_selection_type")
    new_obj.PHIUS2021_heating_demand = _input_dict.get("PHIUS2021_heating_demand")
    new_obj.PHIUS2021_cooling_demand = _input_dict.get("PHIUS2021_cooling_demand")
    new_obj.PHIUS2021_heating_load = _input_dict.get("PHIUS2021_heating_load")
    new_obj.PHIUS2021_cooling_load = _input_dict.get("PHIUS2021_cooling_load")
    new_obj.building_status = _input_dict.get("building_status")
    new_obj.building_type = _input_dict.get("building_type")

    return new_obj


# -- Ground
def _Foundation(_cls, _input_dict):
    new_obj = _cls()

    return new_obj
