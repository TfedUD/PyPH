# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions used to determine infiltation flow rates from the HB Room Objects"""

import honeybee.room
import statistics
import LBT_Utils.boundary_conditions

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
