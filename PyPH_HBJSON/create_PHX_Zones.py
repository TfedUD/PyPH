# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions used to build WUFI Zones and WUFI Rooms based on HB-Model inputs"""

import statistics

import honeybee.room
import PHX.bldg_segment
import PHX.spaces
import PHX.summer_ventilation
import PHX.utilization_patterns
import LBT_Utils.program

# -- Zones
# -------------------------------------------------------------------------------
def create_PHX_Zone_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.bldg_segment.Zone:
    """Creates a new PHX-Zone from a single Honeybee 'Room'.

    Note: This function does not create the 'PHX-Spaces' within the PHX-Zone. Use
    create_PHX_Zones.add_Spaces_from_HB_room() in order to add Spaces if desired.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee room to use as the source for the new PHX-Zone

    Returns:
    --------
        * (PHX.bldg_segment.Zone): The new PHX-Zone object with Attributes based on the Honeybee Room
    """

    zone = PHX.bldg_segment.Zone()
    zone.n = _hb_room.display_name
    zone.identifier = _hb_room.identifier
    zone.source_zone_identifiers.append(_hb_room.identifier)

    if _hb_room.volume:
        zone.volume_gross = _hb_room.volume
        zone.volume_gross_selection = 7  # User defined
        zone.volume_net_selection = 4  # Estimated from gross volume

    if _hb_room.floor_area:
        zone.floor_area = _hb_room.floor_area
        zone.floor_area_selection = 6  # User Determined

    # -- Summer Ventilation Parameters
    zone.summer_ventilation = PHX.summer_ventilation.SummerVent.from_dict(
        _hb_room.user_data.get("phx", {}).get("summ_vent", {})
    )

    return zone


def set_Space_ventilation_from_HB_room(_hb_room, _phx_Space):
    """Calcs and sets PHX-Space's ventilation flow rates based on the host Honeyebee Room"""

    # - Ventilation Airflow
    total_vent_airflow = LBT_Utils.program.calc_HB_Room_total_ventilation_m3sec(
        _hb_room
    )

    _phx_Space.ventilation.supply = total_vent_airflow * 3600
    _phx_Space.ventilation.extract = total_vent_airflow * 3600
    _phx_Space.ventilation.transfer = 0.0


def create_PHX_Spaces_from_HB_room(_hb_room):
    # type: (honeybee.room.Room) -> list[PHX.spaces.Space]
    """Returns a list of new PHX-Spaces based on the Honeybee Room"""

    # --- Get any detailed user-determined Space info on the HB-Room
    user_determined_space_dict = _hb_room.user_data.get("phx", {}).get("spaces", [])

    spaces = []
    if user_determined_space_dict:
        # --- Build new Spaces based on the User-determiend detailed inputs
        for space_dict in user_determined_space_dict.values():

            new_phx_space = PHX.spaces.Space.from_dict(space_dict)

            spaces.append(new_phx_space)
    else:
        # --- Build a default space if no detailed ones provided
        new_phx_space = PHX.spaces.Space()
        new_phx_space.space_number = None
        new_phx_space.space_name = f"{_hb_room.display_name}_room"

        set_Space_ventilation_from_HB_room(_hb_room, new_phx_space)
        spaces.append(new_phx_space)

    return spaces


# -- Schedules
# ----
"""This is included only to cache the  schedules, so don't have to recompute 8760 hourly values each time."""
schedules_infiltration = {}


def get_infiltration_schdedule_annual_avg(_hb_room: honeybee.room.Room):
    """Returns the Honeybee room's infiltration average annual reduction rate, as per the Honeybee Schedule"""

    sched_identifier = _hb_room.properties.energy.infiltration.schedule.identifier
    if sched_identifier in schedules_infiltration.keys():
        # -- If the schedules has already been computed, just use that one
        # -- This is just done to speed up the overall calculation.
        return schedules_infiltration[sched_identifier]
    else:
        # -- Otherwise, computer the annual average value
        schedule = _hb_room.properties.energy.infiltration.schedule
        sched_avg_value = statistics.mean(schedule.data_collection().values)

        # -- And add it to the colletion
        schedules_infiltration[sched_identifier] = sched_avg_value
        return sched_avg_value


def calc_HB_room_infiltration(_hb_room: honeybee.room.Room) -> float:
    """Return the annual average infiltration airlow rate (m3/h) of the Honeybee Room

    Note: This value takes into account the Infiltration rate and the Schedule
    """

    avg_reduction_factor = get_infiltration_schdedule_annual_avg(_hb_room)

    room_peak_airflow_m3_s_m2 = (
        _hb_room.properties.energy.infiltration.flow_per_exterior_area
    )
    room_exterior_m2 = _hb_room.exposed_area
    room_peak_airflow_m3_s = room_peak_airflow_m3_s_m2 * room_exterior_m2
    room_peak_airflow_m3_h = room_peak_airflow_m3_s * 3600
    room_annual_avg_airflow_m3_h = room_peak_airflow_m3_h * avg_reduction_factor

    return room_annual_avg_airflow_m3_h


def add_default_res_appliance_to_zone(
    _wp_zone: PHX.bldg_segment.Zone,
) -> PHX.bldg_segment.Zone:
    return None
    dw = Appliance_KitchenDishwasher()
    _wp_zone.add_new_appliance(dw)

    return _wp_zone
