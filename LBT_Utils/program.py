# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for working with Ladybug-Tools objects"""

import honeybee.room
import statistics


def clean_HB_program_name(_name):
    # type: (str) -> str
    """Cleans the HB program / Schedule name

    ie: "2013::MutiFam::Corridor" --> "Corridor"
    "Corrior_People" --> "Corridor"
    """
    clean = str(_name).split("::")[-1]
    clean = str(clean).replace("_People", "")
    clean = str(clean).replace("_Lighting", "")
    return clean


def calc_HB_Room_avg_occupancy(_hb_room):
    # type: (honeybee.room.Room ) -> float
    """Returns the 'average' HB Room occupancy"""

    # -- Figure out the max occupancy (Num of People)
    if _hb_room.properties.energy.people:
        # Not all Honeybee programs have an Occupancy, like Stairs for example
        peak_occupancy_per_area = _hb_room.properties.energy.people.people_per_area
    else:
        return 0

    peak_occupancy = peak_occupancy_per_area * _hb_room.floor_area

    # -- Calc the Program's mean_occupancy, if needed
    if not hasattr(_hb_room.properties.energy.people.occupancy_schedule, "mean_occupancy"):
        # Get the hourly occupancy as list of 8760 decimal values ie: [0.6, 0.65 0.78, 0.93,...]
        mean_occupancy = statistics.mean(_hb_room.properties.energy.people.occupancy_schedule.values())
    else:
        mean_occupancy = _hb_room.properties.energy.people.occupancy_schedule.mean_occupancy

    return peak_occupancy * mean_occupancy


def calc_HB_Room_total_ventilation_m3sec(_hb_room):
    # type: (honeybee.room.Room) -> float
    """Returns the total peak ventilation airflow for a Honeybee Room

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee Room to calculate values of.

    Returns:
    --------
        * (float): The Honeybee Room's total ventilation airflow in M3/second.
    """

    flow_per_ach = _hb_room.properties.energy.ventilation.air_changes_per_hour * _hb_room.volume
    flow_per_area = _hb_room.properties.energy.ventilation.flow_per_area * _hb_room.floor_area
    flow_per_zone = _hb_room.properties.energy.ventilation.flow_per_zone
    room_avg_occupancy = calc_HB_Room_avg_occupancy(_hb_room)
    flow_per_person = _hb_room.properties.energy.ventilation.flow_per_person * room_avg_occupancy

    total_vent = 0.0
    total_vent += flow_per_ach
    total_vent += flow_per_area
    total_vent += flow_per_zone
    total_vent += flow_per_person

    return total_vent


def calc_HB_room_avg_ventilation_ach(_hb_room):
    # type: (honeybee.room.Room) -> float
    """Returns the honeybee room's average annual ACH due to ventilation.

    This value includes the effect of mechanical ventilation and windows, and the
    variation in occupancy (assumes demand-controlled ventilation flow rates) but
    excludes infiltration.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room)

    Returns:
    --------
        * (float) The Room's ventilation average annual ACH (air changes per hour)
    """

    # -- First, find the average anuual flow-fraction
    hb_ventilation_schedule = _hb_room.properties.energy.ventilation.schedule
    if not hb_ventilation_schedule:
        avg_flow_fraction = 1.0
    else:
        avg_flow_fraction = 0.0  # Need func

    # -- Calc the annual average airflow (m3/h)
    design_airflow_m3s = calc_HB_Room_total_ventilation_m3sec(_hb_room)
    design_airflow_m3h = design_airflow_m3s * 3600
    avg_annual_flow = design_airflow_m3h * avg_flow_fraction

    return avg_annual_flow / _hb_room.volume
