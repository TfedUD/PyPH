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


def _generate_histogram(_data, _num_bins):
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


def calc_four_part_vent_sched_values_from_hb_room(_hb_room, _use_dcv=False):
    # type: (honeybee.room.Room, bool) -> dict
    """Returns a PH-Style four_part schedule values for the Ventilation airflow, based on the HB Room.

    Arguments:
    ----------
        * _hb_room (): The Honyebee Room to build the schedule for.
        * _dcv (bool): Demand-Controled Ventilation. default=False. Set True in
            order to take the Occupancy Schedule and Airflow-per-person loads into account

    Returns:
    --------
        * dict: The four_part Sched values. * dict: ie: {0:{'average_value (m3s)':12, 'frequency':0.25}, 1:{...}, ...}
    """

    # 1) Get the Peak Occupancy Loads
    if _hb_room.properties.energy.people is not None:
        people_per_m2 = _hb_room.properties.energy.people.people_per_area
        num_ppl = people_per_m2 * _hb_room.floor_area
    else:
        num_ppl = 0

    # 2) Get/Calc the Peak Airflow Loads from Ventilation
    if _hb_room.properties.energy.ventilation is not None:
        vent_m3s_for_zone = _hb_room.properties.energy.ventilation.flow_per_zone
        vent_m3s_for_area = _hb_room.properties.energy.ventilation.flow_per_area * _hb_room.floor_area
        vent_m3h_for_ach = (_hb_room.properties.energy.ventilation.air_changes_per_hour * _hb_room.volume) / 3600
        vent_m3s_total = vent_m3s_for_zone + vent_m3s_for_area + vent_m3h_for_ach

        occ_m3s_total = _hb_room.properties.energy.ventilation.flow_per_person * num_ppl
    else:
        vent_m3s_total = 0
        occ_m3s_total = 0

    # 3) Get the Ventilation Schedules
    if (
        _hb_room.properties.energy.people is not None
        and _hb_room.properties.energy.people.occupancy_schedule is not None
    ):
        schd_occ_values = _hb_room.properties.energy.people.occupancy_schedule.data_collection()
    else:
        # If there is no Occupancy Schedule, assume constant airflow (?)
        schd_occ_values = (1 for _ in range(8760))

    # 4) Get the Ventilation Schedules
    if (
        _hb_room.properties.energy.ventilation is not None
        and _hb_room.properties.energy.ventilation.schedule is not None
    ):
        schd_vent_values = _hb_room.properties.energy.ventilation.schedule.data_collection()
    else:
        # If there is no Ventilation Schedule, that means constant airflow
        schd_vent_values = (1 for _ in range(8760))

    # 3) Calc the Hourly Airflows, taking the Schedules into account
    hourly_m3s_for_vent = (vent_m3s_total * _ for _ in schd_vent_values)
    if _use_dcv:
        hourly_m3s_for_occ = (occ_m3s_total * _ for _ in schd_occ_values)
    else:
        hourly_m3s_for_occ = (occ_m3s_total * 0 for _ in schd_occ_values)

    # 4) Calc the Percentage of Peak airflow for each hourly value
    peak_total_m3s = vent_m3s_total + occ_m3s_total
    if peak_total_m3s == 0:
        return {0: {"average_value": 1.0, "frequency": 1.0}}

    hourly_total_vent_percentage_rate = (
        (a + b) / peak_total_m3s for a, b in zip(hourly_m3s_for_vent, hourly_m3s_for_occ)
    )

    # 5) Histogram that shit
    four_part_sched_dict = _generate_histogram(
        _data=list(hourly_total_vent_percentage_rate),
        _num_bins=4,
    )

    return four_part_sched_dict
