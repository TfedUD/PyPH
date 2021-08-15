# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions used to build WUFI Zones and WUFI Rooms based on HB-Model inputs"""

import statistics

import honeybee.room
import PHX.bldg_segment
import PHX.spaces
import PHX.summer_ventilation
import PHX.utilization_patterns
import PHX.occupancy
import LBT_Utils.program
import LBT_Utils.boundary_conditions

# -- Zones
# ------------------------------------------------------------------------------
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

    # -- Occupany Parameters
    occ_dict = _hb_room.user_data.get("phx", {}).get("zone_occupancy", {})
    zone.occupancy = PHX.occupancy.ZoneOccupancy.from_dict(occ_dict)

    return zone


def set_Space_ventilation_from_HB_room(_hb_room, _phx_Space):
    """Calcs and sets PHX-Space's ventilation flow rates based on the host Honeyebee Room"""

    # - Ventilation Airflow
    total_vent_airflow = LBT_Utils.program.calc_HB_Room_total_ventilation_m3sec(_hb_room)

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


# -- Infiltration
# ------------------------------------------------------------------------------
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


def calc_airflow_at_test_pressure(_flow_at_standard_p: float) -> float:
    """Returns the infiltration airflow (m3/s) at test pressure (normally 50Pa).

    Reverses the Honeybee 'Blower Pressure Converter' calculation.
    Convert infiltration airflow at 'normal' pressure (~4Pa) back to airflow at test pressure (50Pa)

    HB Equation:
          _flow_at_standard_p = C_qa * (test_pressure ** flow_expoent)
          C_qa = (flow_per_exterior_at_test_p * air_density) / (test_pressure ** flow_exponent)

    Rearrange to solve for infilt_at_test_p:
        C_qa = _flow_at_standard_p / (test_pressure ** flow_expoent)
        flow_per_exterior_at_test_p = (C_qa * (test_pressure ** flow_exponent))/air_density

    Arguments:
    ----------
        * _flow_at_standard_p (float): (m3-s/m2) Infiltration airflow, per m2 of envelope,
            at standard building pressure (~4Pa).

    Returns:
    --------
        * (float): (m3/s-m2) Infiltration airflow, per m2 of envelope, at test building pressure (50Pa)
    """

    air_density = 1.0
    flow_exponent = 0.65
    test_pressure = 50  # Pa
    bldg_pressure = 4  # Pa

    C_qa = _flow_at_standard_p / (bldg_pressure ** flow_exponent)
    flow_per_exterior_at_test_p = (C_qa * (test_pressure ** flow_exponent)) / air_density

    return flow_per_exterior_at_test_p


def calc_HB_room_infiltration(_hb_room: honeybee.room.Room) -> float:
    """Returns the annual average infiltration airflow (m3/s) at blower-door test pressure"""

    # -- Calc the peak airflow at test pressure
    peak_airflow_per_exterior_at_test_p = calc_airflow_at_test_pressure(
        _hb_room.properties.energy.infiltration.flow_per_exterior_area
    )

    # -- Calc the annual average airflow at test pressure
    avg_annual_reduction_factor = get_infiltration_schdedule_annual_avg(_hb_room)
    room_exterior_m2 = LBT_Utils.boundary_conditions.hb_room_PHX_exposed_area(_hb_room)
    room_peak_airflow_m3s = peak_airflow_per_exterior_at_test_p * room_exterior_m2
    room_annual_avg_airflow_m3s = room_peak_airflow_m3s * avg_annual_reduction_factor

    return room_annual_avg_airflow_m3s


def add_default_res_appliance_to_zone(
    _wp_zone: PHX.bldg_segment.Zone,
) -> PHX.bldg_segment.Zone:
    return None
    dw = Appliance_KitchenDishwasher()
    _wp_zone.add_new_appliance(dw)

    return _wp_zone
