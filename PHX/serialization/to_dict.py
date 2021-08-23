# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
Functions for converting PHX Objects to serializable text dictionaries. All PHX Objects
should be able to be converted to fully text represenations.
"""

# -- Utilization Patterns
def _VentilationUtilization(_obj):
    d = {}

    d.update({"daily_op_sched": _obj.daily_op_sched})
    d.update({"frac_of_design_airflow": _obj.frac_of_design_airflow})

    return d


def _VentilationUtilizations(_obj):  # Collection
    d = {}

    d.update({"maximum": _obj.maximum.to_dict()})
    d.update({"standard": _obj.standard.to_dict()})
    d.update({"basic": _obj.basic.to_dict()})
    d.update({"minimum": _obj.minimum.to_dict()})

    return d


# -- Utilization Patterns
def _UtilizationPattern_Ventilation(_obj):
    d = {}

    d.update({"id": _obj.id})
    d.update({"n": _obj.n})
    d.update({"OperatingDays": _obj.OperatingDays})
    d.update({"OperatingWeeks": _obj.OperatingWeeks})

    d.update({"utilizations": _obj.utilizations.to_dict()})

    return d


def _UtilPat_Occupancy(_obj):
    d = {}
    return d


def UtilPat_Lighting(_obj):
    d = {}
    return d


# -- Ventilation
def _SummerVent(_obj):
    d = {}

    d.update({"avg_mech_ach": _obj.avg_mech_ach})
    d.update({"day_window_ach": _obj.day_window_ach})
    d.update({"night_window_ach": _obj.night_window_ach})
    d.update({"additional_mech_ach": _obj.additional_mech_ach})
    d.update({"additional_mech_spec_power": _obj.additional_mech_spec_power})
    d.update({"exhaust_ach": _obj.exhaust_ach})
    d.update({"exhaust_spec_power": _obj.exhaust_spec_power})
    d.update({"additional_mech_control_mode": _obj.additional_mech_control_mode})
    d.update({"avg_mech_control_mode": _obj.avg_mech_control_mode})

    return d


# -- HVAC
def _PropertiesVentilation(_obj):
    d = {}

    d.update({"airflows": _obj.airflows.to_dict()})
    d.update({"ventilator": _obj.ventilator.to_dict()})
    d.update({"utilization_pattern": _obj.utilization_pattern.to_dict()})

    return d


def _HVAC_Ventilation_Airflows(_obj):
    d = {}

    d.update({"supply": _obj.supply})
    d.update({"extract": _obj.extract})
    d.update({"transfer": _obj.transfer})

    return d


def _HVAC_PH_Parameters(_obj):
    d = {}

    d.update({"HumidityRecoveryEfficiency": _obj.HumidityRecoveryEfficiency})
    d.update({"ElectricEfficiency": _obj.ElectricEfficiency})
    d.update({"FrostProtection": _obj.FrostProtection})
    d.update({"Quantity": _obj.Quantity})
    d.update({"SubsoilHeatExchangeEfficiency": _obj.SubsoilHeatExchangeEfficiency})
    d.update({"HumidityRecoveryEfficiency": _obj.HumidityRecoveryEfficiency})
    d.update({"VolumeFlowRateFrom": _obj.VolumeFlowRateFrom})
    d.update({"VolumeFlowRateTo": _obj.VolumeFlowRateTo})
    d.update({"TemperatureBelowDefrostUsed": _obj.TemperatureBelowDefrostUsed})
    d.update({"DefrostRequired": _obj.DefrostRequired})
    d.update({"NoSummerBypass": _obj.NoSummerBypass})
    d.update({"HRVCalculatorData": _obj.HRVCalculatorData})
    d.update({"Maximum_VOS": _obj.Maximum_VOS})
    d.update({"Maximum_PP": _obj.Maximum_PP})
    d.update({"Standard_VOS": _obj.Standard_VOS})
    d.update({"Standard_PP": _obj.Standard_PP})
    d.update({"Basic_VOS": _obj.Basic_VOS})
    d.update({"Basic_PP": _obj.Basic_PP})
    d.update({"Minimum_VOS": _obj.Minimum_VOS})
    d.update({"Minimum_PP": _obj.Minimum_PP})
    d.update({"AuxiliaryEnergy": _obj.AuxiliaryEnergy})
    d.update({"AuxiliaryEnergyDHW": _obj.AuxiliaryEnergyDHW})
    d.update({"InConditionedSpace": _obj.InConditionedSpace})

    return d


def _HVAC_Device(_obj):
    d = {}

    d.update({"id": _obj.id})
    d.update({"identifier": str(_obj.identifier)})
    d.update({"Name": _obj.Name})
    d.update({"SystemType": _obj.SystemType})
    d.update({"TypeDevice": _obj.TypeDevice})
    d.update({"UsedFor_Heating": _obj.UsedFor_Heating})
    d.update({"UsedFor_DHW": _obj.UsedFor_DHW})
    d.update({"UsedFor_Cooling": _obj.UsedFor_Cooling})
    d.update({"UsedFor_Ventilation": _obj.UsedFor_Ventilation})
    d.update({"UsedFor_Humidification": _obj.UsedFor_Humidification})
    d.update({"UsedFor_Dehumidification": _obj.UsedFor_Dehumidification})
    d.update({"Ventilation_Parameters": _obj.Ventilation_Parameters})
    d.update({"UseOptionalClimate": _obj.UseOptionalClimate})
    d.update({"IdentNr_OptionalClimate": _obj.IdentNr_OptionalClimate})
    d.update({"PH_Parameters": _obj.PH_Parameters.to_dict()})

    return d


def _HVAC_System(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"id": _obj.id})
    d.update({"n": _obj.n})
    d.update({"typeSys": _obj.typeSys})
    d.update({"lZoneCover": _obj.lZoneCover})
    d.update({"_device_dict": _obj._device_dict})
    d.update({"distrib": _obj.distrib})
    d.update({"suppDev": _obj.suppDev})
    d.update({"PHdistrib": _obj.PHdistrib})

    return d


# -- HVAC: Ventilation
def _HVAC_Ventilation_Duct_Segment(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"length": _obj.length})
    d.update({"diameter": _obj.diameter})
    d.update({"width": _obj.width})
    d.update({"height": _obj.height})
    d.update({"insulation_thickness": _obj.insulation_thickness})
    d.update({"insulation_conductivity": _obj.insulation_conductivity})

    return d


def _HVAC_Ventilation_Duct(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"segments": [seg.to_dict() for seg in _obj.segments]})

    return d


def _HVAC_Ventilation_System(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"type": _obj.type})
    d.update({"ventilator": _obj.ventilator.to_dict()})
    d.update({"duct_01": _obj.duct_01.to_dict()})
    d.update({"duct_02": _obj.duct_02.to_dict()})

    return d


# -- Spaces
def _FloorSegment(_obj):
    d = {}

    d.update({"weighting_factor": _obj.weighting_factor})
    d.update({"floor_area_gross": _obj.floor_area_gross})
    d.update({"space_name": _obj.space_name})
    d.update({"space_number": _obj.space_number})
    d.update({"non_res_lighting": _obj.non_res_lighting})
    d.update({"non_res_motion": _obj.non_res_motion})
    d.update({"non_res_usage": _obj.non_res_usage})
    d.update({"_ventilation": _obj._ventilation.to_dict()})
    d.update({"host_zone_identifier": _obj.host_zone_identifier})

    geometry_dict = {}
    for _ in _obj.geometry:
        geometry_dict.update({id(_): _.to_dict()})
    d.update({"geometry": geometry_dict})

    return d


def _Floor(_obj):
    d = {}

    d.update({"space_name": _obj.space_name})
    d.update({"space_number": _obj.space_number})
    d.update({"non_res_lighting": _obj.non_res_lighting})
    d.update({"non_res_motion": _obj.non_res_motion})
    d.update({"non_res_usage": _obj.non_res_usage})
    d.update({"_ventilation": _obj._ventilation.to_dict()})
    d.update({"host_zone_identifier": _obj.host_zone_identifier})

    floor_segments_dict = {}
    for flr_seg in _obj.floor_segments:
        floor_segments_dict.update({id(flr_seg): flr_seg.to_dict()})
    d.update({"floor_segments": floor_segments_dict})

    return d


def _Volume(_obj):
    d = {}

    d.update({"space_name": _obj.space_name})
    d.update({"space_number": _obj.space_number})
    d.update({"host_zone_identifier": _obj.host_zone_identifier})
    d.update({"_average_ceiling_height": _obj._average_ceiling_height})
    d.update({"_volume": _obj._volume})

    d.update({"floor": _obj.floor.to_dict()})

    d.update({"_ventilation": _obj._ventilation.to_dict()})

    volume_geometry_dict = {}
    for list_of_geom in _obj.volume_geometry:
        geom_list = {}
        for geom in list_of_geom:
            geom_list.update({id(geom): geom.to_dict()})
        volume_geometry_dict.update({id(geom_list): geom_list})

    d.update({"volume_geometry": volume_geometry_dict})

    return d


def _Space(_obj):
    d = {}

    d.update({"space_name": _obj.space_name})
    d.update({"space_number": _obj.space_number})
    d.update({"host_zone_identifier": _obj.host_zone_identifier})
    d.update({"occupancy": _obj.occupancy})
    d.update({"equipment": _obj.equipment})
    d.update({"ventilation": _obj.ventilation.to_dict()})
    d.update({"occupancy": _obj.occupancy.to_dict()})

    d.update({"volume": _obj.volume})

    volumes_dict = {}
    for volume in _obj.volumes:
        volumes_dict.update({id(volume): volume.to_dict()})
    d.update({"volumes": volumes_dict})

    return d


# -- Occupany
def _BldgSegmentOccupancy(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"category": _obj.category})
    d.update({"usage_type": _obj.usage_type})
    d.update({"num_units": _obj.num_units})
    d.update({"num_stories": _obj.num_stories})

    return d


def _ZoneOccupancy(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"num_occupants": _obj.num_occupants})
    d.update({"num_bedrooms": _obj.num_bedrooms})
    d.update({"num_dwelling_units": _obj.num_dwelling_units})

    return d


def _SpaceOccupancy(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"start_hour": _obj.start_hour})
    d.update({"end_hour": _obj.end_hour})
    d.update({"annual_utilization_days": _obj.annual_utilization_days})
    d.update({"relative_absence": _obj.relative_absence})
    d.update({"people_per_area =": _obj.people_per_area})

    return d


# -- Passive House Certification
def _PHIUSCertification(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"certification_criteria": _obj.certification_criteria})
    d.update({"localization_selection_type": _obj.localization_selection_type})
    d.update({"PHIUS2021_heating_demand": _obj.PHIUS2021_heating_demand})
    d.update({"PHIUS2021_cooling_demand": _obj.PHIUS2021_cooling_demand})
    d.update({"PHIUS2021_heating_load": _obj.PHIUS2021_heating_load})
    d.update({"PHIUS2021_cooling_load": _obj.PHIUS2021_cooling_load})
    d.update({"building_status": _obj.building_status})
    d.update({"building_type": _obj.building_type})

    return d


# -- Ground
def _Foundation(_obj):
    d = {}

    return d


# -- Appliances
def _ApplianceSet(_obj):
    d = {}

    for appliance in _obj.appliances:
        if not appliance:
            continue

        appliance_name = _obj.known_types.get(appliance.type)
        d.update({appliance_name: appliance.to_dict()})

    return d


def _Appliance(_obj):
    d = {}

    d.update({"type": _obj.type})
    d.update({"reference_quantity": _obj.reference_quantity})
    d.update({"quantity": _obj.quantity})
    d.update({"in_conditioned_space": _obj.in_conditioned_space})
    d.update({"reference_energy_norm": _obj.reference_energy_norm})
    d.update({"energy_demand": _obj.energy_demand})
    d.update({"energy_demand_per_use": _obj.energy_demand_per_use})
    d.update({"combined_energy_facor": _obj.combined_energy_facor})

    # -- Dishwasher
    d.update({"dishwasher_capacity_type": _obj.dishwasher_capacity_type})
    d.update({"dishwasher_capacity": _obj.dishwasher_capacity})
    d.update({"dishwasher_water_connection": _obj.dishwasher_water_connection})

    # -- Laundry Washer
    d.update({"washer_capacity": _obj.washer_capacity})
    d.update({"washer_modified_energy_factor": _obj.washer_modified_energy_factor})
    d.update({"washer_connection": _obj.washer_connection})

    # -- Laundry Dryer
    d.update({"dryer_type": _obj.dryer_type})
    d.update({"dryer_gas_consumption": _obj.dryer_gas_consumption})
    d.update({"dryer_gas_efficiency_factor": _obj.dryer_gas_efficiency_factor})
    d.update({"dryer_field_utilization_factor_type": _obj.dryer_field_utilization_factor_type})
    d.update({"dryer_field_utilization_factor": _obj.dryer_field_utilization_factor})

    # -- Cooktop
    d.update({"cooktop_type": _obj.cooktop_type})

    # -- PHIUS Lighting
    d.update({"lighting_frac_high_efficiency": _obj.lighting_frac_high_efficiency})
    d.update({"user_defined_total": _obj.user_defined_total})

    return d


# -- Lighting
def _SpaceLighting(_obj):
    d = {}

    d.update({"name": _obj.name})
    d.update({"identifier": str(_obj.identifier)})

    return d
