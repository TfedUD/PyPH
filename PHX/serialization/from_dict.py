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
import PHX.spaces
import PHX.climate
import PHX.programs.schedules
import PHX.programs.loads
import PHX.appliances
import PHX.programs.occupancy
import PHX.programs.lighting
import PHX.programs.ventilation
import PHX.mechanicals.systems
import PHX.mechanicals.equipment
import LBT_Utils.geometry


def _setattr_filter(_obj, _attr_name, _attr_val, _filter=True):
    """Normal setattr() but with a filter in front to catch null values"""

    if _attr_val is None and _filter:
        return None
    else:
        setattr(_obj, _attr_name, _attr_val)
        return None


# ------------------------------------------------------------------------------
# ------- PROGRAMS --------
def _RoomLighting(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.schedule = PHX.programs.schedules.Schedule_Lighting.from_dict(_input_dict.get("schedule", {}))
    new_obj.loads = PHX.programs.loads.Load_Lighting.from_dict(_input_dict.get("loads", {}))

    return new_obj


def _RoomVentilation(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.schedule = PHX.programs.schedules.Schedule_Ventilation.from_dict(_input_dict.get("schedule", {}))
    new_obj.loads = PHX.programs.loads.Load_Ventilation.from_dict(_input_dict.get("loads", {}))

    return new_obj


def _RoomOccupancy(_cls, _input_dict):
    new_obj = _cls()

    new_obj.id = _input_dict.get("id")
    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.schedule = PHX.programs.schedules.Schedule_Occupancy.from_dict(_input_dict.get("schedule", {}))
    new_obj.loads = PHX.programs.loads.Load_Occupancy.from_dict(_input_dict.get("loads", {}))

    return new_obj


def _RoomElectricEquipment(_cls, _input_dict):
    new_obj = _cls()

    new_obj.id = _input_dict.get("id")
    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.schedule = PHX.programs.schedules.Schedule_ElecEquip.from_dict(_input_dict.get("schedule", {}))
    new_obj.loads = PHX.programs.loads.Load_ElecEquip.from_dict(_input_dict.get("loads", {}))

    return new_obj


def _BldgSegmentOccupancy(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.category = _input_dict.get("category")
    new_obj.usage_type = _input_dict.get("usage_type")
    new_obj.num_units = _input_dict.get("num_units")
    new_obj.num_stories = _input_dict.get("num_stories")

    return new_obj


def _ZoneOccupancy(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.num_occupants = _input_dict.get("num_occupants", 0)
    new_obj.num_bedrooms = _input_dict.get("num_bedrooms", 0)
    new_obj.num_dwelling_units = _input_dict.get("num_dwelling_units", 0)

    return new_obj


# ------------------------------------------------------------------------------
# ------- Schedules and Utilization Rates  -------
def _Vent_UtilRate(_cls, _input_dict):
    new_obj = _cls()

    new_obj.daily_op_sched = _input_dict.get("daily_op_sched")
    new_obj.frac_of_design_airflow = _input_dict.get("frac_of_design_airflow")

    return new_obj


def _Vent_UtilRates(_cls, _input_dict):  # Collection
    new_obj = _cls()

    new_obj.maximum = PHX.programs.schedules.Vent_UtilRate.from_dict(_input_dict.get("maximum", {}))
    new_obj.standard = PHX.programs.schedules.Vent_UtilRate.from_dict(_input_dict.get("standard", {}))
    new_obj.basic = PHX.programs.schedules.Vent_UtilRate.from_dict(_input_dict.get("basic", {}))
    new_obj.minimum = PHX.programs.schedules.Vent_UtilRate.from_dict(_input_dict.get("minimum", {}))

    return new_obj


def _Schedule_Ventilation(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.name = _input_dict.get("name")
    new_obj.operating_days = _input_dict.get("operating_days")
    new_obj.operating_weeks = _input_dict.get("operating_weeks")
    new_obj.utilization_rates = PHX.programs.schedules.Vent_UtilRates.from_dict(
        _input_dict.get("utilization_rates", {})
    )

    return new_obj


def _Schedule_Occupancy(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.name = _input_dict.get("name")
    new_obj.start_hour = _input_dict.get("start_hour")
    new_obj.end_hour = _input_dict.get("end_hour")
    new_obj.annual_utilization_days = _input_dict.get("annual_utilization_days")
    new_obj.relative_utilization_factor = _input_dict.get("relative_utilization_factor")

    return new_obj


def _Schedule_Lighting(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.name = _input_dict.get("name")
    new_obj.daily_operating_hours = _input_dict.get("daily_operating_hours")
    new_obj.annual_utilization_days = _input_dict.get("annual_utilization_days")
    new_obj.relative_utilization_factor = _input_dict.get("relative_utilization_factor")

    return new_obj


def _Schedule_ElecEquip(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.name = _input_dict.get("name")
    new_obj.annual_utilization_factor = _input_dict.get("annual_utilization_factor")

    return new_obj


def _Schedule_NonResAppliance(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.name = _input_dict.get("name")
    new_obj.start_hour = _input_dict.get("start_hour")
    new_obj.end_hour = _input_dict.get("end_hour")
    new_obj.annual_utilization_days = _input_dict.get("annual_utilization_days")
    new_obj.relative_utilization_factor = _input_dict.get("relative_utilization_factor")

    return new_obj


# ------------------------------------------------------------------------------
# ------- Loads  -------
def _Load_Lighting(_cls, _input_dict):
    new_obj = _cls()

    new_obj.name = _input_dict.get("name")
    new_obj.target_lux = _input_dict.get("target_lux")
    new_obj.target_lux_height = _input_dict.get("target_lux_height")
    new_obj.watts_per_area = _input_dict.get("watts_per_area")

    return new_obj


def _Load_Ventilation(_cls, _input_dict):
    new_obj = _cls()

    new_obj.name = _input_dict.get("name")
    new_obj.supply = _input_dict.get("supply")
    new_obj.extract = _input_dict.get("extract")
    new_obj.transfer = _input_dict.get("transfer")

    return new_obj


def _Load_Occupancy(_cls, _input_dict):
    new_obj = _cls()

    new_obj.name = _input_dict.get("name")
    new_obj.people_per_area = _input_dict.get("people_per_area")

    return new_obj


def _Load_ElecEquip(_cls, _input_dict):
    new_obj = _cls()

    new_obj.name = _input_dict.get("name")
    new_obj.watts_per_area = _input_dict.get("watts_per_area")

    return new_obj


# ------------------------------------------------------------------------------
# ------- GEOMETRY --------
def _Vector(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.x = _input_dict.get("x")
    new_obj.y = _input_dict.get("y")
    new_obj.z = _input_dict.get("z")

    return new_obj


def _Vertex(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.x = _input_dict.get("x")
    new_obj.y = _input_dict.get("y")
    new_obj.z = _input_dict.get("z")

    return new_obj


def _Polygon(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj._nVec = PHX.geometry.Vector.from_dict(_input_dict.get("_nVec", {}))
    new_obj._area = _input_dict.get("_area")
    new_obj.idPolyI = _input_dict.get("idPolyI")
    new_obj.children = _input_dict.get("children")

    for _ in _input_dict.get("vertices", {}).values():
        new_obj.vertices.append(PHX.geometry.Vertex.from_dict(_))

    return new_obj


# ------------------------------------------------------------------------------
# ------- HVAC --------
# -- HVAC: System
def _Mechanicals(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    system_dicts = _input_dict.get("_systems", [])
    for system_dict in system_dicts:
        new_obj.add_system(PHX.mechanicals.systems.MechanicalSystem.from_dict(system_dict))

    return new_obj


def _MechanicalSystem(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.id = _input_dict.get("id")
    new_obj.name = _input_dict.get("name")
    new_obj.system_group_type_number = _input_dict.get("system_group_type_number")
    new_obj.lZoneCover = _input_dict.get("lZoneCover")
    new_obj.equipment_set = PHX.mechanicals.equipment.EquipmentSet.from_dict(_input_dict.get("equipment_set", {}))
    new_obj.system_usage = PHX.mechanicals.systems.HVAC_System_Usage.from_dict(_input_dict.get("system_usage", {}))

    return new_obj


def _HVAC_System_Usage(_cls, _input_dict):
    new_obj = _cls()

    new_obj.used_for_heating = _input_dict.get("used_for_heating")
    new_obj.used_for_DHW = _input_dict.get("used_for_DHW")
    new_obj.used_for_cooling = _input_dict.get("used_for_cooling")
    new_obj.used_for_ventilation = _input_dict.get("used_for_ventilation")
    new_obj.used_for_humidification = _input_dict.get("used_for_humidification")
    new_obj.used_for_dehumidification = _input_dict.get("used_for_dehumidification")
    new_obj.used_optional_climate = _input_dict.get("used_optional_climate")
    new_obj.optional_climate_id_number = _input_dict.get("optional_climate_id_number")

    return new_obj


# -- HVAC: Equipment
def _EquipmentSet(_cls, _input_dict):
    new_obj = _cls()

    new_obj.id = _input_dict.get("id")
    new_obj.identifier = _input_dict.get("identifier")

    equipment_dicts = _input_dict.get("equipment", [])
    for equipment_dict in equipment_dicts:

        # -- Try and get the right 'Type' of Device from_dict() constructor.
        # -- Will default to generic "HVAC Device" if no constructor is found or if error
        try:
            device_type_name = equipment_dict.get("_class_name_", "HVAC_Device")
            from_dict_constructor = "PHX.mechanicals.equipment.{}.from_dict(equipment_dict)".format(device_type_name)
            new_equipment = eval(from_dict_constructor)
        except Exception:
            new_equipment = PHX.mechanicals.equipment.HVAC_Device.from_dict(equipment_dict)

        new_obj.add_new_device_to_equipment_set(new_equipment)

    return new_obj


def _HVAC_Device(_cls, _input_dict):
    new_obj = _cls()

    new_obj.id = _input_dict.get("id")
    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.device_type = _input_dict.get("device_type")
    new_obj.system_type = _input_dict.get("system_type")
    new_obj.properties = PHX.mechanicals.equipment.HVAC_Device_Properties.from_dict(_input_dict.get("properties", {}))

    return new_obj


def _HVAC_Device_Properties(_cls, _input_dict):
    new_obj = _cls()

    for k, v in _input_dict.items():
        setattr(new_obj, k, v)

    return new_obj


# -- HVAC: Equipment : Ventilation
def _HVAC_Ventilator(_cls, _input_dict):
    new_obj = _cls()

    new_obj.id = _input_dict.get("id")
    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.device_type = _input_dict.get("device_type")
    new_obj.system_type = _input_dict.get("system_type")
    new_obj.properties = PHX.mechanicals.equipment.HVAC_Device_Properties.from_dict(_input_dict.get("properties", {}))

    return new_obj


def _HVAC_Duct_Segment(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.length = _input_dict.get("length")
    new_obj.diameter = _input_dict.get("diameter")
    new_obj.width = _input_dict.get("width")
    new_obj.height = _input_dict.get("height")
    new_obj.insulation_thickness = _input_dict.get("insulation_thickness")
    new_obj.insulation_conductivity = _input_dict.get("insulation_conductivity")

    return new_obj


def _HVAC_Duct(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    for d in _input_dict.get("segments", []):
        new_obj.segments.append(PHX.hvac_components.HVAC_Duct_Segment.from_dict(d))

    return new_obj


# -- HVAC: Summer Vent
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


# -- HW: Equipment
def _HW_Tank(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.device_type = _input_dict.get("device_type")
    new_obj.system_type = _input_dict.get("system_type")
    new_obj.properties = PHX.mechanicals.equipment.HVAC_Device_Properties.from_dict(_input_dict.get("properties", {}))

    return new_obj


def _HW_Heater_Direct_Elec(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("name")
    new_obj.device_type = _input_dict.get("device_type")
    new_obj.system_type = _input_dict.get("system_type")
    new_obj.properties = PHX.mechanicals.equipment.HVAC_Device_Properties.from_dict(_input_dict.get("properties", {}))

    return new_obj


# ------------------------------------------------------------------------------
# ------- Space / Zones  -------
# -- Spaces
def _FloorSegment(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj._weighting_factor = _input_dict.get("_weighting_factor")
    new_obj._floor_area_gross = _input_dict.get("_floor_area_gross")
    new_obj.space_name = _input_dict.get("space_name")
    new_obj.space_number = _input_dict.get("space_number")
    new_obj.host_zone_identifier = _input_dict.get("host_zone_identifier")

    for d in _input_dict.get("geometry", {}).values():
        # -- Allows for both LBT geometry and PHX geometry
        try:
            geom = LBT_Utils.geometry.LBT_geometry_dict_util(d)
        except LBT_Utils.geometry.LBTGeometryTypeError:
            geom = PHX.geometry.Polygon.from_dict(d)
        new_obj.geometry.append(geom)

    vent_load_dict = _input_dict.get("_ventilation_loads")
    if vent_load_dict:
        new_obj.ventilation_loads = PHX.programs.loads.Load_Ventilation.from_dict(vent_load_dict)

    return new_obj


def _Floor(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.space_name = _input_dict.get("space_name")
    new_obj.space_number = _input_dict.get("space_number")
    new_obj.host_zone_identifier = _input_dict.get("host_zone_identifier")

    new_obj.floor_segments = []
    for flr_seg_dict in _input_dict.get("floor_segments", {}).values():
        if flr_seg_dict:
            new_flr_seg = PHX.spaces.FloorSegment.from_dict(flr_seg_dict)
            new_obj.floor_segments.append(new_flr_seg)

    vent_load_dict = _input_dict.get("_ventilation_loads")
    if vent_load_dict:
        new_obj.ventilation_loads = PHX.programs.loads.Load_Ventilation.from_dict(vent_load_dict)

    return new_obj


def _Volume(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
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
            # -- Allows for both LBT geometry and PHX geometry
            try:
                new_geom = LBT_Utils.geometry.LBT_geometry_dict_util(__)
            except LBT_Utils.geometry.LBTGeometryTypeError:
                new_geom = PHX.geometry.Polygon.from_dict(__)
            new_geom_list.append(new_geom)
        new_obj.volume_geometry.append(new_geom_list)

    return new_obj


def _Space(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.volume = _input_dict.get("volume")  # Number
    new_obj.volumes = []  # Volume Objects
    for volume_dict in _input_dict.get("volumes", {}).values():
        new_obj.volumes.append(PHX.spaces.Volume.from_dict(volume_dict))

    new_obj.space_name = _input_dict.get("space_name")
    new_obj.space_number = _input_dict.get("space_number")
    new_obj.host_zone_identifier = _input_dict.get("host_zone_identifier")

    vent_load_dict = _input_dict.get("_ventilation_loads")
    if vent_load_dict:
        new_obj.ventilation_loads = PHX.programs.loads.Load_Ventilation.from_dict(vent_load_dict)

    return new_obj


# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# -- Climate
def _Climate(_cls, _input_dict):
    new_obj = _cls()

    new_obj.name = _input_dict.get("name")
    new_obj.summer_daily_temperature_swing = _input_dict.get("summer_daily_temperature_swing")
    new_obj.average_wind_speed = _input_dict.get("average_wind_speed")

    new_obj.location = PHX.climate.Climate_Location.from_dict(_input_dict.get("location", {}))
    new_obj.ground = PHX.climate.Climate_Ground.from_dict(_input_dict.get("ground", {}))

    new_obj.monthly_temperature_air = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_temperature_air", {})
    )
    new_obj.monthly_temperature_dewpoint = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_temperature_dewpoint", {})
    )
    new_obj.monthly_temperature_sky = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_temperature_sky", {})
    )
    new_obj.monthly_temperature_ground = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_temperature_ground", {})
    )

    new_obj.monthly_radiation_north = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_radiation_north", {})
    )
    new_obj.monthly_radiation_east = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_radiation_east", {})
    )
    new_obj.monthly_radiation_south = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_radiation_south", {})
    )
    new_obj.monthly_radiation_west = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_radiation_west", {})
    )
    new_obj.monthly_radiation_global = PHX.climate.Climate_MonthlyValueCollection.from_dict(
        _input_dict.get("monthly_radiation_global", {})
    )

    new_obj.peak_heating_1 = PHX.climate.Climate_PeakLoadCollection.from_dict(_input_dict.get("peak_heating_1", {}))
    new_obj.peak_heating_2 = PHX.climate.Climate_PeakLoadCollection.from_dict(_input_dict.get("peak_heating_2", {}))
    new_obj.peak_cooling = PHX.climate.Climate_PeakLoadCollection.from_dict(_input_dict.get("peak_cooling", {}))

    return new_obj


def _Climate_Ground(_cls, _input_dict):
    new_obj = _cls()

    new_obj.ground_thermal_conductivity = _input_dict.get("ground_thermal_conductivity")
    new_obj.ground_heat_capacitiy = _input_dict.get("ground_heat_capacitiy")
    new_obj.ground_density = _input_dict.get("ground_density")
    new_obj.depth_groundwater = _input_dict.get("depth_groundwater")
    new_obj.flow_rate_groundwater = _input_dict.get("flow_rate_groundwater")

    return new_obj


def _Climate_Location(_cls, _input_dict):
    new_obj = _cls()

    new_obj.latitude = _input_dict.get("latitude")
    new_obj.longitude = _input_dict.get("longitude")
    new_obj.weather_station_elevation = _input_dict.get("weather_station_elevation")
    new_obj.climate_zone = _input_dict.get("climate_zone")
    new_obj.hours_from_UTC = _input_dict.get("hours_from_UTC")

    return new_obj


def _Climate_PeakLoadCollection(_cls, _input_dict):
    new_obj = _cls()

    new_obj.temp = _input_dict.get("temp")
    new_obj.rad_north = _input_dict.get("rad_north")
    new_obj.rad_east = _input_dict.get("rad_east")
    new_obj.rad_south = _input_dict.get("rad_south")
    new_obj.rad_west = _input_dict.get("rad_west")
    new_obj.rad_global = _input_dict.get("rad_global")

    return new_obj


def _Climate_MonthlyValueCollection(_cls, _input_dict):
    new_obj = _cls()

    new_obj.january = _input_dict.get("january")
    new_obj.february = _input_dict.get("february")
    new_obj.march = _input_dict.get("march")
    new_obj.april = _input_dict.get("april")
    new_obj.may = _input_dict.get("may")
    new_obj.june = _input_dict.get("june")
    new_obj.july = _input_dict.get("july")
    new_obj.august = _input_dict.get("august")
    new_obj.september = _input_dict.get("september")
    new_obj.october = _input_dict.get("october")
    new_obj.november = _input_dict.get("november")
    new_obj.december = _input_dict.get("december")

    return new_obj


# ------------------------------------------------------------------------------
# -- Ground
def _Foundation(_cls, _input_dict):
    new_obj = _cls()

    return new_obj


# ------------------------------------------------------------------------------
# -- Assemblies
def _Material(_cls, _input_dict):
    new_obj = _cls()

    new_obj.identifier = _input_dict.get("identifier")
    new_obj.name = _input_dict.get("n")
    new_obj.tConD = _input_dict.get("tConD")
    new_obj.densB = _input_dict.get("densB")
    new_obj.hCapS = _input_dict.get("hCapS")

    return new_obj


def _Layer(_cls, _input_dict):
    new_obj = _cls()

    return new_obj


def _Assembly(_cls, _input_dict):
    new_obj = _cls()

    return new_obj


# ------------------------------------------------------------------------------
# -- Appliances
def _ApplianceSet(_cls, _input_dict):
    new_obj = _cls()

    for appliance_type_dict in _input_dict.values():
        for appliance_dict in appliance_type_dict.values():
            appliance_obj = PHX.appliances.Appliance.from_dict(appliance_dict)
            new_obj.add_appliances_to_set(appliance_obj)

    return new_obj


def _Appliance(_cls, _input_dict):
    if not _input_dict:
        return None

    new_obj = _cls()

    _setattr_filter(new_obj, "name", _input_dict.get("name"))
    _setattr_filter(new_obj, "type", _input_dict.get("type"))
    _setattr_filter(new_obj, "comment", _input_dict.get("comment"))
    _setattr_filter(new_obj, "reference_quantity", _input_dict.get("reference_quantity"))
    _setattr_filter(new_obj, "quantity", _input_dict.get("quantity"))
    _setattr_filter(new_obj, "in_conditioned_space", _input_dict.get("in_conditioned_space"))
    _setattr_filter(new_obj, "reference_energy_norm", _input_dict.get("reference_energy_norm"))
    _setattr_filter(new_obj, "energy_demand", _input_dict.get("energy_demand"))
    _setattr_filter(new_obj, "energy_demand_per_use", _input_dict.get("energy_demand_per_use"))
    _setattr_filter(new_obj, "combined_energy_facor", _input_dict.get("combined_energy_facor"))

    # -- Dishwasher
    _setattr_filter(new_obj, "dishwasher_capacity_type", _input_dict.get("dishwasher_capacity_type"))
    _setattr_filter(new_obj, "dishwasher_capacity", _input_dict.get("dishwasher_capacity"))
    _setattr_filter(new_obj, "dishwasher_water_connection", _input_dict.get("dishwasher_water_connection"))

    # -- Laundry Washer
    _setattr_filter(new_obj, "washer_capacity", _input_dict.get("washer_capacity"))
    _setattr_filter(new_obj, "washer_modified_energy_factor", _input_dict.get("washer_modified_energy_factor"))
    _setattr_filter(new_obj, "washer_connection", _input_dict.get("washer_connection"))

    # -- Laundry Dryer
    _setattr_filter(new_obj, "dryer_type", _input_dict.get("dryer_type"))
    _setattr_filter(new_obj, "dryer_gas_consumption", _input_dict.get("dryer_gas_consumption"))
    _setattr_filter(new_obj, "dryer_gas_efficiency_factor", _input_dict.get("dryer_gas_efficiency_factor"))
    _setattr_filter(
        new_obj, "dryer_field_utilization_factor_type", _input_dict.get("dryer_field_utilization_factor_type")
    )
    _setattr_filter(new_obj, "dryer_field_utilization_factor", _input_dict.get("dryer_field_utilization_factor"))

    # -- Cooktop
    _setattr_filter(new_obj, "cooktop_type", _input_dict.get("cooktop_type"))

    # -- PHIUS Lighting
    _setattr_filter(new_obj, "lighting_frac_high_efficiency", _input_dict.get("lighting_frac_high_efficiency"))
    _setattr_filter(new_obj, "_user_defined_total", _input_dict.get("_user_defined_total"))

    # -- PHIUS Non-Res Kitchen
    _setattr_filter(new_obj, "num_meals_per_day", _input_dict.get("num_meals_per_day"))
    usage_sched_dict = _input_dict.get("usage", None)
    if usage_sched_dict:
        new_obj.usage = PHX.programs.schedules.Schedule_NonResAppliance.from_dict(usage_sched_dict)

    return new_obj
