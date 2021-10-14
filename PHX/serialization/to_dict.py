# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
Functions for converting PHX Objects to serializable text dictionaries. All PHX Objects
should be able to be converted to fully text represenations.
"""

import json

# -- Base
def __Base(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"user_data": _obj.user_data})

    return d


# ------------------------------------------------------------------------------
# ------- PROGRAMS --------
def _RoomLighting(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"schedule": _obj.schedule.to_dict()})
    d.update({"loads": _obj.loads.to_dict()})

    return d


def _RoomElectricEquipment(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"schedule": _obj.schedule.to_dict()})
    d.update({"loads": _obj.loads.to_dict()})

    return d


def _RoomVentilation(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"schedule": _obj.schedule.to_dict()})
    d.update({"loads": _obj.loads.to_dict()})

    return d


def _RoomOccupancy(_obj):
    d = {}

    d.update({"id": _obj.id})
    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"schedule": _obj.schedule.to_dict()})
    d.update({"loads": _obj.loads.to_dict()})

    return d


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


# ------------------------------------------------------------------------------
# ------- Schedules and Utilization Rates  -------
def _Vent_UtilRate(_obj):
    d = {}

    d.update({"daily_op_sched": _obj.daily_op_sched})
    d.update({"frac_of_design_airflow": _obj.frac_of_design_airflow})

    return d


def _Vent_UtilRates(_obj):  # Collection
    d = {}

    d.update({"maximum": _obj.maximum.to_dict()})
    d.update({"standard": _obj.standard.to_dict()})
    d.update({"basic": _obj.basic.to_dict()})
    d.update({"minimum": _obj.minimum.to_dict()})

    return d


def _Schedule_Ventilation(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"id": _obj.id})
    d.update({"name": _obj.name})
    d.update({"operating_days": _obj.operating_days})
    d.update({"operating_weeks": _obj.operating_weeks})
    d.update({"utilization_rates": _obj.utilization_rates.to_dict()})

    return d


def _Schedule_Occupancy(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"id": _obj.id})
    d.update({"name": _obj.name})
    d.update({"start_hour": _obj.start_hour})
    d.update({"end_hour": _obj.end_hour})
    d.update({"annual_utilization_days": _obj.annual_utilization_days})
    d.update({"relative_utilization_factor": _obj.relative_utilization_factor})

    return d


def _Schedule_Lighting(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"id": _obj.id})
    d.update({"name": _obj.name})
    d.update({"daily_operating_hours": _obj.daily_operating_hours})
    d.update({"annual_utilization_days": _obj.annual_utilization_days})
    d.update({"relative_utilization_factor": _obj.relative_utilization_factor})

    return d


def _Schedule_ElecEquip(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"id": _obj.id})
    d.update({"name": _obj.name})
    d.update({"annual_utilization_factor": _obj.annual_utilization_factor})

    return d


# ------------------------------------------------------------------------------
# ------- Loads  -------
def _Load_Lighting(_obj):
    d = {}

    d.update({"name": _obj.name})
    d.update({"target_lux": _obj.target_lux})
    d.update({"target_lux_height": _obj.target_lux_height})
    d.update({"watts_per_area": _obj.watts_per_area})

    return d


def _Load_Ventilation(_obj):
    d = {}

    d.update({"name": _obj.name})
    d.update({"supply": _obj.supply})
    d.update({"extract": _obj.extract})
    d.update({"transfer": _obj.transfer})

    return d


def _Load_Occupancy(_obj):
    d = {}

    d.update({"name": _obj.name})
    d.update({"people_per_area": _obj.people_per_area})

    return d


def _Load_ElecEquip(_obj):
    d = {}

    d.update({"name": _obj.name})
    d.update({"watts_per_area": _obj.watts_per_area})

    return d


# ------------------------------------------------------------------------------
# ------- GEOMETRY --------
def _Vector(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"x": _obj.x})
    d.update({"y": _obj.y})
    d.update({"z": _obj.z})

    return d


def _Vertex(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"id": _obj.id})
    d.update({"x": _obj.x})
    d.update({"y": _obj.y})
    d.update({"z": _obj.z})

    return d


def _Polygon(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"id": _obj.id})
    d.update({"_nVec": _obj._nVec.to_dict()})
    d.update({"_area": _obj._area})
    d.update({"idPolyI": _obj.idPolyI})
    d.update({"children": _obj.children})

    vertex_dict = {}
    for _ in _obj.vertices:
        vertex_dict.update({str(_.identifier): _.to_dict()})
    d.update({"vertices": vertex_dict})

    return d


# ------------------------------------------------------------------------------
# ------- HVAC --------
# -- HVAC: System
def _Mechanicals(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})

    system_dicts = []
    for system in _obj.systems:
        system_dicts.append(system.to_dict())
    d.update({"_systems": system_dicts})

    return d


def _MechanicalSystem(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"id": _obj.id})
    d.update({"name": _obj.name})
    d.update({"system_group_type_number": _obj.system_group_type_number})
    d.update({"lZoneCover": _obj.lZoneCover})
    d.update({"equipment_set": _obj.equipment_set.to_dict()})
    # d.update({"distribution": _obj.distribution.to_dict()})
    d.update({"system_usage": _obj.system_usage.to_dict()})

    return d


def _HVAC_System_Usage(_obj):
    d = {}

    d.update({"used_for_heating": _obj.used_for_heating})
    d.update({"used_for_DHW": _obj.used_for_DHW})
    d.update({"used_for_cooling": _obj.used_for_cooling})
    d.update({"used_for_ventilation": _obj.used_for_ventilation})
    d.update({"used_for_humidification": _obj.used_for_humidification})
    d.update({"used_for_dehumidification": _obj.used_for_dehumidification})
    d.update({"used_optional_climate": _obj.used_optional_climate})
    d.update({"optional_climate_id_number": _obj.optional_climate_id_number})

    return d


# -- HVAC: Equipment
def _EquipmentSet(_obj):
    d = {}

    d.update({"id": _obj.id})
    d.update({"identifier": str(_obj.identifier)})

    equipment_dicts = []
    for equipment in _obj.equipment:
        equipment_dicts.append(equipment.to_dict())
    d.update({"equipment": equipment_dicts})

    return d


def _HVAC_Device(_obj):
    d = {}

    d.update({"id": _obj.id})
    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"device_type": _obj.device_type})
    d.update({"system_type": _obj.system_type})
    d.update({"_class_name_": _obj.__class__.__name__})
    d.update({"properties": _obj.properties.to_dict()})

    return d


def _HVAC_Device_Properties(_obj):
    d = {}

    for k, v in _obj.__dict__.items():
        try:
            json.dumps({k: v})
            d.update({k: v})
        except TypeError:
            d.update({k: str(v)})

    return d


# -- HVAC: Equipment : Ventilation
def _HVAC_Ventilator(_obj):
    d = {}

    d.update({"id": _obj.id})
    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"device_type": _obj.device_type})
    d.update({"system_type": _obj.system_type})
    d.update({"_class_name_": _obj.__class__.__name__})
    d.update({"properties": _obj.properties.to_dict()})

    return d


def _HVAC_Duct_Segment(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"length": _obj.length})
    d.update({"diameter": _obj.diameter})
    d.update({"width": _obj.width})
    d.update({"height": _obj.height})
    d.update({"insulation_thickness": _obj.insulation_thickness})
    d.update({"insulation_conductivity": _obj.insulation_conductivity})

    return d


def _HVAC_Duct(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"segments": [seg.to_dict() for seg in _obj.segments]})

    return d


# -- HVAC: SummerVent
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


# -- HW: Equipment


def _HW_Tank(_obj):
    d = {}

    d.update({"id": _obj.id})
    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"device_type": _obj.device_type})
    d.update({"system_type": _obj.system_type})
    d.update({"_class_name_": _obj.__class__.__name__})
    d.update({"properties": _obj.properties.to_dict()})

    return d


def _HW_Heater_Direct_Elec(_obj):
    d = {}

    d.update({"id": _obj.id})
    d.update({"identifier": str(_obj.identifier)})
    d.update({"name": _obj.name})
    d.update({"device_type": _obj.device_type})
    d.update({"system_type": _obj.system_type})
    d.update({"_class_name_": _obj.__class__.__name__})
    d.update({"properties": _obj.properties.to_dict()})

    return d


# ------------------------------------------------------------------------------
# -- Spaces
def _FloorSegment(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"_weighting_factor": _obj._weighting_factor})
    d.update({"_floor_area_gross": _obj._floor_area_gross})
    d.update({"space_name": _obj.space_name})
    d.update({"space_number": _obj.space_number})

    d.update({"host_zone_identifier": _obj.host_zone_identifier})

    geometry_dict = {}
    for i, geom in enumerate(_obj.geometry):
        geometry_dict.update({i: geom.to_dict()})
    d.update({"geometry": geometry_dict})

    if _obj.ventilation_loads:
        d.update({"_ventilation_loads": _obj.ventilation_loads.to_dict()})

    return d


def _Floor(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"space_name": _obj.space_name})
    d.update({"space_number": _obj.space_number})

    d.update({"host_zone_identifier": _obj.host_zone_identifier})

    floor_segments_dict = {}
    for i, flr_seg in enumerate(_obj.floor_segments):
        floor_segments_dict.update({i: flr_seg.to_dict()})
    d.update({"floor_segments": floor_segments_dict})

    if _obj.ventilation_loads:
        d.update({"_ventilation_loads": _obj.ventilation_loads.to_dict()})

    return d


def _Volume(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"space_name": _obj.space_name})
    d.update({"space_number": _obj.space_number})
    d.update({"host_zone_identifier": _obj.host_zone_identifier})
    d.update({"_average_ceiling_height": _obj._average_ceiling_height})
    d.update({"_volume": _obj._volume})

    d.update({"floor": _obj.floor.to_dict()})

    volume_geometry_dict = {}
    for k, list_of_geom in enumerate(_obj.volume_geometry):
        geom_list = {}
        for i, geom in enumerate(list_of_geom):
            geom_list.update({i: geom.to_dict()})
        volume_geometry_dict.update({k: geom_list})

    d.update({"volume_geometry": volume_geometry_dict})

    return d


def _Space(_obj):
    d = {}

    d.update({"identifier": str(_obj.identifier)})
    d.update({"space_name": _obj.space_name})
    d.update({"space_number": _obj.space_number})
    d.update({"host_zone_identifier": _obj.host_zone_identifier})

    d.update({"volume": _obj.volume})

    volumes_dict = {}
    for i, volume in enumerate(_obj.volumes):
        volumes_dict.update({i: volume.to_dict()})
    d.update({"volumes": volumes_dict})

    if _obj.ventilation_loads:
        d.update({"_ventilation_loads": _obj.ventilation_loads.to_dict()})

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


# ------------------------------------------------------------------------------
# -- Ground
def _Foundation(_obj):
    d = {}

    return d


# ------------------------------------------------------------------------------
# -- Assemblies
def _Material(_obj):
    d = {}

    return d


def _Layer(_obj):
    d = {}

    return d


def _Assembly(_obj):
    d = {}

    return d


# ------------------------------------------------------------------------------
# -- Appliances
def _ApplianceSet(_obj):
    d = {}

    for appliance_type_name, appliances in _obj.appliance_dict.items():
        type_dict = {}
        for i, appliance in enumerate(appliances):
            type_dict[i] = appliance.to_dict()
        d[appliance_type_name] = type_dict

    return d


def _Appliance(_obj):
    d = {}

    d.update({"type": _obj.type})
    d.update({"comment": _obj.comment})
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
    d.update({"_user_defined_total": _obj._user_defined_total})

    return d
