# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to convert data from PHX objects into WUFI-specific format.

These functions area used before building the XML Write Schema and are used
to reorganize / restructure the PHX data to match the funny WUFI configuration.
"""

from PHX.bldg_segment import Zone, Room, BldgSegment, PHIUSCertification
from PHX.project import Project
from PHX.climate import Climate
from PHX.mechanicals.systems import Mechanicals, MechanicalSystem
from PHX.mechanicals.equipment import HVAC_Device
from PyPH_WUFI.WUFI_xml_conversion_classes import (
    UtilizationPattern_Vent,
    UtilizationPatternCollection_Vent,
    UtilizationPattern_NonRes,
    UtilizationPatternCollection_NonRes,
    temp_RoomVentilation,
    temp_Space,
    temp_Zone,
    temp_Project,
    temp_MechanicalSystemsGroup,
    temp_MechanicalDevice,
    temp_Mechanicals,
    temp_Climate,
    temp_PH_Building,
    temp_PH_Building_Internal_Gains,
    temp_PH_Building_Internal_Gains_Data,
    temp_Building,
    temp_PassiveHouseData,
)

TOL = 2  # Value tolerance for rounding. ie; 9.84318191919 -> 9.84

# ------------------------------------------------------------------------------
# -- HRV ID
def build_temp_RoomVentilation(_phx_object: Room) -> temp_RoomVentilation:
    """Find the Fresh-air Ventilator ID number which serves the PHX-Room

    Arguments:
    ----------
        * (PHX.bldg_segment.Room):

    Returns:
    --------
        * (temp_RoomVentilation):
    """

    temp_room_vent = temp_RoomVentilation()

    for mech_sys in _phx_object.mechanicals.systems:
        ventilator_type_number = 1
        for d in mech_sys.equipment_set.get_all_devices_by_type(ventilator_type_number):
            temp_room_vent.ventilator_id = d.id

    return temp_room_vent


# ------------------------------------------------------------------------------
# -- Build all the Spaces with the Room Program attributes
def build_temp_Zone(_phx_zone: Zone) -> temp_Zone:
    """Since Program and Equipment are only present at the 'Room' level, need to add
    that info to the Spaces so that can be written out properly to WUFI.
    """

    temp_zone = temp_Zone()

    for room in _phx_zone.rooms:
        for base_space in room.spaces:
            # Calc % of total floor area, for lighting.
            # What the fuck WUFI???? You can't just use floor area?
            space_percent_floor_area_total = base_space.floor_area_weighted / _phx_zone.floor_area

            new_space = temp_Space(
                space=base_space,
                ventilation=room.ventilation,
                lighting=room.lighting,
                occupancy=room.occupancy,
                elec_equipment=room.electric_equipment,
                mechanicals=room.mechanicals,
                space_percent_floor_area_total=space_percent_floor_area_total,
            )

            # Preserve the Space-level flow rates, if they exist
            # instead of the Room-level flow rates
            if new_space.space.ventilation_loads:
                new_space.ventilation.loads.supply = base_space.ventilation_loads.supply
                new_space.ventilation.loads.extract = base_space.ventilation_loads.extract
                new_space.ventilation.loads.transfer = base_space.ventilation_loads.transfer

            temp_zone.spaces.append(new_space)

    return temp_zone


# ------------------------------------------------------------------------------
# -- Project, Utilization Factors
def build_temp_NonRes_UtilCollection_from_zones(_zones: list[Zone]):
    """Collects and builds the Non-Res Utilization Patterns (occupancy, lighting) found on the Zone's Rooms

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the PHX-Zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes)
    """

    util_collection = UtilizationPatternCollection_NonRes()

    for zone in _zones:
        for room in zone.rooms:
            util_pattern = UtilizationPattern_NonRes()
            util_pattern.occupancy = room.occupancy
            util_pattern.lighting = room.lighting
            pattern_id = util_pattern.occupancy.unique_key + util_pattern.lighting.unique_key

            util_collection.add_to_collection(util_pattern, _key=pattern_id, _reset_count=True)
            room.occupancy.id = util_pattern.id
            room.lighting.id = util_pattern.id

    return util_collection


def build_temp_vent_UtilCollection_from_zones(_zones: list[Zone]) -> UtilizationPatternCollection_Vent:
    """Collects and builds the Ventilation Utilization Patterns found on the Zone's Rooms

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the PHX-Zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (UtilizationPatternCollection_Vent)
    """

    # Create the new Util Pattern Collection
    util_collection = UtilizationPatternCollection_Vent()

    for zone in _zones:
        for room in zone.rooms:
            # Build the UtilizationPattern based on the Space, add it to the collection
            util_pattern = UtilizationPattern_Vent()

            util_pattern.name = room.ventilation.schedule.name
            util_pattern.operating_days = room.ventilation.schedule.operating_days
            util_pattern.operating_weeks = room.ventilation.schedule.operating_weeks
            util_pattern.utilization_rates = room.ventilation.schedule.utilization_rates

            util_pattern.force_max_utilization_hours(_max_hours=24.0)

            key = room.ventilation.schedule.identifier
            util_collection.add_to_collection(util_pattern, _key=key, _reset_count=True)
            room.ventilation.schedule.id = util_pattern.id  # Reset the Room Vent id to match

    return util_collection


def build_temp_Project(_phx_project: Project) -> temp_Project:
    """Create the WUFI 'Utilization Pattern' Collections from the schedules and loads"""

    temp_project = temp_Project()

    temp_project.util_pattern_collection_non_residential = build_temp_NonRes_UtilCollection_from_zones(
        _phx_project.zones
    )
    temp_project.util_pattern_collection_ventilation = build_temp_vent_UtilCollection_from_zones(_phx_project.zones)

    return temp_project


# ------------------------------------------------------------------------------
# -- HVAC Systems
def build_temp_HVAC_Device_from_PHX_Equipment(_phx_device: HVAC_Device) -> temp_MechanicalDevice:
    """Return a new WUFI temp_MechanicalDevice bassed on an input PHX-Equipment.

    Arguments:
    ----------
        * _phx_device (PHX.mechanicals.equipment.HVAC_Device): The PHX-HVAC_Device to
            use as the source for the new WUFI Device.

    Returns:
    --------
        * (temp_MechanicalDevice): A new WUFI Device, based on the PHX input device.
    """

    t = temp_MechanicalDevice()

    t.name = _phx_device.name
    t.id = _phx_device.id
    t.device_type = _phx_device.device_type
    t.system_type = _phx_device.system_type
    t.properties = _phx_device.properties

    return t


def build_temp_HVAC_Devices_from_PHX_Sys(_phx_system: MechanicalSystem) -> list[temp_MechanicalDevice]:
    """For WUFI, each piece of equipment in a PHX-System needs to become
    its own 'Device' up the top-level of the System-Group.

    Arguments:
    ----------
        * _phx_system (PHX.mechanicals.systems.MechanicalSystem): The PHX-System
            to build the WUFI Devices from. Each piece of equipment in the
            equiment-set will be converted into its own 'Device'

    Returns:
    --------
        * (list[temp_MechanicalDevice]): A list of the new WUFI Devices,
            built from the PHX System.
    """

    wufi_devices = []

    for equipment in _phx_system.equipment_set.equipment:
        t = build_temp_HVAC_Device_from_PHX_Equipment(equipment)  # Conversion function
        t.system_usage = _phx_system.system_usage
        wufi_devices.append(t)

    return wufi_devices


def build_temp_Mechanicals(_phx_mechanicals: Mechanicals) -> temp_Mechanicals:
    """Sort the PHX Mechanical Systems by 'Group Type'

    Arguments:
    ----------
        * _phx_mechanicals (PHX.mechanicals.systems.Mechanicals): The PHX 'Mechanicals' objetct to use.

    Returns:
    --------
        * (temp_Mechanicals): The Temp 'Mechanicals' with the systems grouped and re-organized.
    """

    tM = temp_Mechanicals()

    for phx_sys in _phx_mechanicals.systems:
        if phx_sys.system_group_type_number not in tM._mech_groups.keys():
            tGr = temp_MechanicalSystemsGroup()
            tGr.group_type_number = phx_sys.system_group_type_number
            tM._mech_groups[phx_sys.system_group_type_number] = tGr
        else:
            tGr = tM._mech_groups[phx_sys.system_group_type_number]

        wufi_devices = build_temp_HVAC_Devices_from_PHX_Sys(phx_sys)
        tGr.wufi_devices.extend(wufi_devices)

    return tM


#  ------------------------------------------------------------------------------
# -- Climate
def build_temp_Climate(_phx_climate: Climate) -> temp_Climate:

    tCl = temp_Climate()
    tCl.PH_Climate.summer_daily_temperature_swing = _phx_climate.summer_daily_temperature_swing
    tCl.PH_Climate.average_wind_speed = _phx_climate.average_wind_speed

    tCl.PH_Climate.location = _phx_climate.location
    tCl.PH_Climate.ground = _phx_climate.ground

    tCl.PH_Climate.monthly_temperature_air = _phx_climate.monthly_temperature_air
    tCl.PH_Climate.monthly_temperature_dewpoint = _phx_climate.monthly_temperature_dewpoint
    tCl.PH_Climate.monthly_temperature_sky = _phx_climate.monthly_temperature_sky
    tCl.PH_Climate.monthly_temperature_ground = _phx_climate.monthly_temperature_ground

    tCl.PH_Climate.monthly_radiation_north = _phx_climate.monthly_radiation_north
    tCl.PH_Climate.monthly_radiation_east = _phx_climate.monthly_radiation_east
    tCl.PH_Climate.monthly_radiation_south = _phx_climate.monthly_radiation_south
    tCl.PH_Climate.monthly_radiation_west = _phx_climate.monthly_radiation_west
    tCl.PH_Climate.monthly_radiation_global = _phx_climate.monthly_radiation_global

    tCl.PH_Climate.peak_heating_1 = _phx_climate.peak_heating_1
    tCl.PH_Climate.peak_heating_2 = _phx_climate.peak_heating_2
    tCl.PH_Climate.peak_cooling = _phx_climate.peak_cooling

    return tCl


# -- BldgSegment
def build_Building(_phx_bldg_segment: BldgSegment) -> temp_Building:
    temp_bldg = temp_Building()

    temp_bldg.numerics = _phx_bldg_segment.numerics
    temp_bldg.airflow_model = _phx_bldg_segment.airflow_model
    temp_bldg.count_generator = _phx_bldg_segment.count_generator
    temp_bldg.has_been_generated = _phx_bldg_segment.has_been_generated
    temp_bldg.has_been_changed_since_last_gen = _phx_bldg_segment.has_been_changed_since_last_gen
    temp_bldg.components = _phx_bldg_segment.components
    temp_bldg.zones = _phx_bldg_segment.zones

    return temp_bldg


def build_PH_Internal_Gains(_phx_Certification: PHIUSCertification) -> temp_PH_Building_Internal_Gains:
    # -- build Internal Gains Data
    temp_int_gains_data = temp_PH_Building_Internal_Gains_Data()
    temp_int_gains_data.int_gains_evap_per_person = _phx_Certification.int_gains_evap_per_person
    temp_int_gains_data.int_gains_flush_heat_loss = _phx_Certification.int_gains_flush_heat_loss
    temp_int_gains_data.int_gains_num_toilets = _phx_Certification.int_gains_num_toilets
    temp_int_gains_data.int_gains_toilet_room_util_pat = _phx_Certification.int_gains_toilet_room_util_pat
    temp_int_gains_data.int_gains_use_school_defaults = _phx_Certification.int_gains_use_school_defaults
    temp_int_gains_data.int_gains_dhw_marginal_perf_ratio = _phx_Certification.int_gains_dhw_marginal_perf_ratio

    # -- build Internal Gains Obj
    temp_int_gains = temp_PH_Building_Internal_Gains()
    temp_int_gains.data = temp_int_gains_data

    return temp_int_gains


def build_PH_Building(_phx_bldg_segment: BldgSegment) -> temp_PH_Building:
    # -- Internal Gains
    temp_int_gains = build_PH_Internal_Gains(_phx_bldg_segment.PHIUS_certification)

    # -- PH_Building
    temp_PH_Bldg = temp_PH_Building()
    temp_PH_Bldg.id = _phx_bldg_segment.id
    temp_PH_Bldg.occupancy_category = _phx_bldg_segment.occupancy.category
    temp_PH_Bldg.occupancy_type = _phx_bldg_segment.occupancy.usage_type
    temp_PH_Bldg.building_status = _phx_bldg_segment.PHIUS_certification.building_status
    temp_PH_Bldg.building_type = _phx_bldg_segment.PHIUS_certification.building_type
    temp_PH_Bldg.occupancy_setting_method = 2
    temp_PH_Bldg.num_units = _phx_bldg_segment.occupancy.num_units
    temp_PH_Bldg.num_stories = _phx_bldg_segment.occupancy.num_stories
    temp_PH_Bldg.q50 = _phx_bldg_segment.infiltration.q50
    temp_PH_Bldg.n50 = _phx_bldg_segment.infiltration.n50
    temp_PH_Bldg.foundations = _phx_bldg_segment.foundations
    temp_PH_Bldg.int_gains = temp_int_gains
    temp_PH_Bldg.summer_hrv_bypass_mode = 2  # <----

    return temp_PH_Bldg


def build_PassiveHouseData(_phx_bldg_segment: BldgSegment) -> temp_PassiveHouseData:
    temp_phData = temp_PassiveHouseData()

    temp_phData.certification_criteria = _phx_bldg_segment.PHIUS_certification.certification_criteria
    temp_phData.localization_selection_type = _phx_bldg_segment.PHIUS_certification.localization_selection_type
    temp_phData.PHIUS2021_heating_demand = _phx_bldg_segment.PHIUS_certification.PHIUS2021_heating_demand
    temp_phData.PHIUS2021_cooling_demand = _phx_bldg_segment.PHIUS_certification.PHIUS2021_cooling_demand
    temp_phData.PHIUS2021_heating_load = _phx_bldg_segment.PHIUS_certification.PHIUS2021_heating_load
    temp_phData.PHIUS2021_cooling_load = _phx_bldg_segment.PHIUS_certification.PHIUS2021_cooling_load

    temp_PH_Bldg = build_PH_Building(_phx_bldg_segment)
    temp_phData.PH_Buildings = [temp_PH_Bldg]

    return temp_phData
