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


# def _generate_histogram(_data, _num_bins):
#     # type: (Iterator[float], int) -> Dict[int,float]
#     """Creates a Histogram of input data, in n-bins.

#     Arguments:
#     ----------
#         * _data (Iterable[float]): Iterable sequence of float values to use as the source.
#         * _num_bins (int): Number of bins to split the data into.

#     Returns:
#     --------
#         * dict: ie: {0:{'average_value':12, 'count':3, 'frequency':0.25}, 1:{...}, ...}
#     """

#     min_val = min(_data)
#     max_val = max(_data)
#     spread = max_val - min_val
#     data_length = len(_data)
#     binned_data = defaultdict(list)

#     # -- Bin the full data set
#     for d in _data:
#         if spread:
#             normalized_value = (d - min_val) / (max_val - min_val)
#         else:
#             normalized_value = d - min_val

#         value = normalized_value * (_num_bins - 1)
#         bin_number = round(value)
#         binned_data[bin_number].append(round(d, 8))

#     # -- Calc Frequency and Avg-Value for each bin
#     for k, v in binned_data.items():
#         binned_data[k] = {
#             "average_value": sum(v) / len(v) if len(v) > 0 else 0,
#             "count": len(v),
#             "frequency": len(v) / data_length,
#         }

#     for k, v in binned_data.items():
#         binned_data[k].update({"value_frac_of_max": v["average_value"] / (max_val or 1)})

#     binned_data["max_value"] = max_val
#     binned_data["min_value"] = min_val

#     return binned_data


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
        frac_of_max = (((sum(v) / len(v)) if len(v) > 0 else 0) / maximum) if maximum else 0
        if frac_of_max > 1.0:
            frac_of_max = 1.0

        output[k] = {
            "count": len(v),
            "average_value": (sum(v) / len(v)) if len(v) > 0 else 0,
            "frequency": len(v) / len(_data),
            "value_frac_of_max": frac_of_max,
        }
    return output


def calc_four_part_vent_sched_values_from_hb_room(_hb_room):
    """Returns a PH-Style four_part schedule values for the Ventilation airflow, based on the HB Room.

    Arguments:
    ----------
        * _hb_room (): The Honyebee Room to build the schedule for.

    Returns:
    --------
        * dict: The four_part Sched vaues. * dict: ie: {0:{'average_value (m3s)':12, 'count':3, 'frequency':0.25}, 1:{...}, ...}
    """

    # -- Calc the hourly airflow rates based on both Occupancy and Ventilation Schedules
    # -- Sort out the right data to use if Schedules or Loads are missing
    # -- Occupancy --
    if _hb_room.properties.energy.people and _hb_room.properties.energy.people.occupancy_schedule:
        hourly_occ_rates = _hb_room.properties.energy.people.occupancy_schedule.data_collection()
        people_per_area = _hb_room.properties.energy.people.people_per_area
    else:
        # If no Occupancy, means no People in the space
        hourly_occ_rates = (1 for _ in range(8760))
        people_per_area = 0
    # -- Design (Peak) Airflow Rate
    design_airflow_rate_m3s = _hb_room.properties.energy.ventilation.flow_per_person * people_per_area
    hourly_airflow_rate_m3s_for_occupancy = (design_airflow_rate_m3s * _ for _ in hourly_occ_rates)

    # -- Ventilation --
    if _hb_room.properties.energy.ventilation and _hb_room.properties.energy.ventilation.schedule:
        hourly_vent_rates = _hb_room.properties.energy.ventilation.schedule.data_collection()
    else:
        # If no Ventilation Sched, means constant operation
        hourly_vent_rates = (1 for _ in range(8760))
    # -- Design (Peak) Airflow Rate
    design_airflow_rate_m3s = (_hb_room.properties.energy.ventilation.air_changes_per_hour * _hb_room.volume) / 3600
    design_airflow_rate_m3s += _hb_room.properties.energy.ventilation.flow_per_area * _hb_room.floor_area
    design_airflow_rate_m3s += _hb_room.properties.energy.ventilation.flow_per_zone
    hourly_airflow_rate_m3s_for_ventilation = (design_airflow_rate_m3s * _ for _ in hourly_vent_rates)

    # -- Combine the Occupancy-Sched-airflow and the Ventilation-Sched-airflow
    total_hourly_airflow_rates_m3s = (
        a + b for a, b in zip(hourly_airflow_rate_m3s_for_occupancy, hourly_airflow_rate_m3s_for_ventilation)
    )
    four_part_sched_dict = _generate_histogram(_data=list(total_hourly_airflow_rates_m3s), _num_bins=4)

    # -- Clean the schedule. WUFI doesn't allow total FOD airflow to be zero for some reason. Sigh.
    total_frac_airflows = sum(
        v.get("value_frac_of_max") for k, v in four_part_sched_dict.items() if k in {0, 1, 2, 3, 4}
    )
    if total_frac_airflows == 0:
        four_part_sched_dict[0]["value_frac_of_max"] = 1.0

    return four_part_sched_dict
