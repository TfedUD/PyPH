# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for working with Ladybug-Tools objects"""

import honeybee.room
import statistics
from collections import defaultdict

try:
    from itertools import izip as zip
except ImportError:  # will be 3.x series
    pass


def clean_HB_program_name(_name):
    # type: (str) -> str
    """Cleans the HB program / Schedule name

    ie: "2013::MutiFam::Corridor" --> "Corridor"
    "Corrior_People" --> "Corridor"
    """
    if not _name:
        return None

    clean = str(_name).split("::")[-1]
    clean = str(clean).replace("_People", "")
    clean = str(clean).replace("_Lighting", "")
    clean = str(clean).replace("_Ventilation", "")

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

    flow_per_ach = (_hb_room.properties.energy.ventilation.air_changes_per_hour * _hb_room.volume) / 3600
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
    avg_annual_flow_m3h = design_airflow_m3h * avg_flow_fraction

    return avg_annual_flow_m3h / _hb_room.volume


def generate_histogram(_data, _num_bins):
    # type: (Iterator[float], int) -> dict
    """Creates a Histogram of input data, in n-bins.

    Arguments:
    ----------
        * _data (Iterable[float]): Iterable sequence of float values to use as the source.
        * _num_bins (int): Number of bins to split the data into.

    Returns:
    --------
        * dict: ie: {0:{'average_value':12, 'count':3, 'frequency':0.25, 'value_frac_of_max':0.22}, 1:{...}, ...}
    """

    # -- Bin the data
    binned_data = defaultdict(list)
    maximum = max(_data)
    minimum = min(_data)
    range = maximum - minimum

    if range == 0:
        binned_data[0] = _data
    else:
        for d in _data:
            normalized_value = (maximum - d) / range
            bin = round(normalized_value * (_num_bins - 1))
            binned_data[bin].append(d)

    # -- Format the data for output
    output = {}
    for k, v in binned_data.items():
        output[k] = {
            "average_value": (sum(v) / len(v)) if len(v) > 0 else 0,
            "frequency": len(v) / len(_data),
        }
    return output


def hb_room_peak_occupancy(_hb_room):
    # type: (honeybee.room.Room) ->  float
    """Returns a Honeybee room's peak occupancy (number of people).

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The honeyebee room to calculate values for.

    Returns:
    --------
        * (float): The Room's peak occupancy (number of people)
    """

    if _hb_room.properties.energy.people is not None:
        people_per_m2 = _hb_room.properties.energy.people.people_per_area
        return people_per_m2 * _hb_room.floor_area
    else:
        return 0


def _get_schedules_as_values(_hb_room):
    # type: (honeybee.room.Room) -> tuple[Generator, Generator]
    """Returns the Honebee room's Occupancy and Ventilation schedules as 8760 values.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee Room to convert the schedules for.

    Returns:
    --------
        * tuple[Generator, Generator]
            * 0: (Generator) 8760 hourly values of the Ventilation Schedule.
            * 1: (Generator) 8760 hourly values of the Occupancy Schedule.
    """

    # -- Ventilation Schedule
    if (
        _hb_room.properties.energy.ventilation is not None
        and _hb_room.properties.energy.ventilation.schedule is not None
    ):
        schd_vent_values = _hb_room.properties.energy.ventilation.schedule.data_collection()
    else:
        # If there is no Ventilation Schedule, that means constant airflow, so return 1 for all
        schd_vent_values = (1 for _ in range(8760))

    # -- Occupancy Schedule
    if (
        _hb_room.properties.energy.people is not None
        and _hb_room.properties.energy.people.occupancy_schedule is not None
    ):
        schd_occ_values = _hb_room.properties.energy.people.occupancy_schedule.data_collection()
    else:
        # If there is no Occupancy Schedule, that means constant airflow, so return 1 for all
        schd_occ_values = (1 for _ in range(8760))

    return (schd_vent_values, schd_occ_values)


def hb_room_peak_airflows(_hb_room, _peak_occupancy):
    # type: (honeybee.room.Room, float) -> tuple[float, float]
    """Returns a tuple of the peak airflow rates (m3/s) for basic Ventilaton and Occupancy-based Ventilation

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The honeyebee room to calculate values for.
        * _peak_occupancy (float): The peak number of people in the room.

    Returns:
    --------
        * tuple[float, float]
            * 0 : Total airflow  (m3/s) For the Ventilation based airflow (per zone, per area, ach).
            * 1 : Total airflow  (m3/s) For the Occupancy based airflow (per person).
    """

    if _hb_room.properties.energy.ventilation is not None:
        vent_m3s_for_zone = _hb_room.properties.energy.ventilation.flow_per_zone
        vent_m3s_for_area = _hb_room.properties.energy.ventilation.flow_per_area * _hb_room.floor_area
        vent_m3h_for_ach = (_hb_room.properties.energy.ventilation.air_changes_per_hour * _hb_room.volume) / 3600

        vent_m3s_total = vent_m3s_for_zone + vent_m3s_for_area + vent_m3h_for_ach
        occ_m3s_total = _hb_room.properties.energy.ventilation.flow_per_person * _peak_occupancy
    else:
        vent_m3s_total = 0
        occ_m3s_total = 0

    return (vent_m3s_total, occ_m3s_total)


def calc_four_part_vent_sched_values_from_hb_room(_hb_room, _use_dcv=True):
    # type: (honeybee.room.Room, bool) -> dict
    """Returns a PH-Style four_part schedule values for the Ventilation airflow, based on the HB Room.

    Arguments:
    ----------
        * _hb_room (): The Honyebee Room to build the schedule for.
        * _dcv (bool): Demand-Controled Ventilation. default=True. Set True in
            order to take the Occupancy Schedule and Airflow-per-person loads into account.
            If False, will asssume constant airflow for occupancy-related ventilation loads.

    Returns:
    --------
        * dict: The four_part Sched values. * dict: ie: {0:{'average_value (m3s)':12, 'frequency':0.25}, 1:{...}, ...}
    """

    # -------------------------------------------------------------------------
    # 1) Calc the Peak Occupancy Loads
    # 2) Calc the Peak Airflow Loads (for Ventilation, for Occupancy)
    # 3) Convert the Occupancy Schedule to Values
    num_ppl = hb_room_peak_occupancy(_hb_room)
    vent_m3s_total, occ_m3s_total = hb_room_peak_airflows(_hb_room, num_ppl)
    schd_vent_values, schd_occ_values = _get_schedules_as_values(_hb_room)

    # -------------------------------------------------------------------------
    # 4) Calc the Hourly Airflows, taking the Schedules into account
    hourly_m3s_for_vent = (vent_m3s_total * _ for _ in schd_vent_values)
    if _use_dcv:
        # -- Modulate the flow rates based on occupancy level
        hourly_m3s_for_occ = (occ_m3s_total * _ for _ in schd_occ_values)
    else:
        # -- Use constant flow rate, regardless of occupancy level
        hourly_m3s_for_occ = (occ_m3s_total * 1 for _ in schd_occ_values)

    #  -------------------------------------------------------------------------
    # 5) Calc the Percentage of Peak airflow for each hourly value
    peak_total_m3s = vent_m3s_total + occ_m3s_total
    if peak_total_m3s == 0:
        return {0: {"average_value": 1.0, "frequency": 1.0}}

    hourly_total_vent_percentage_rate = [
        (a + b) / peak_total_m3s for a, b in zip(hourly_m3s_for_vent, hourly_m3s_for_occ)
    ]

    #  -------------------------------------------------------------------------
    # 6) Histogram that shit
    four_part_sched_dict = generate_histogram(
        _data=hourly_total_vent_percentage_rate,
        _num_bins=4,
    )

    return four_part_sched_dict
