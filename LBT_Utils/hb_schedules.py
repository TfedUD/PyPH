# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for handling Loads, pulled from Honeybee 'ApplyLoadVals' Grasshopper component"""

from honeybee.typing import clean_and_id_ep_string
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.lib.scheduletypelimits import schedule_type_limit_by_identifier
from ladybug.dt import Date


def calc_utilization_factor(_HB_sched):
    # type: (ScheduleRuleset) -> float
    """Return annual utilization factor based on HB annual schedule.
    (0=always absent, 1=always present)

    Arguments:
    ----------
        * _HB_sched (honeybee_energy.schedule.ruleset.ScheduleRuleset): The Honeybee
            ScheduleRuleset object to calculate the values for.

    Returns:
    --------
        * (float): 0.0-1.0 value representing the average utilization factor.

    """

    return sum(_ for _ in _HB_sched.values()) / len(_HB_sched.values())


def create_hb_constant_schedule(_name, _type_limit="Fractional", _value=1):
    # type: (str, str, float) -> ScheduleRuleset
    """Creates a new Honeybee 'Constant' Schedule

    Arguments:
    ----------
        * _name (str):
        * _type_limit (str): default='Fractional'
        * _value (float): The value to set the Constant Schedule to. Default=1

    Returns:
    --------
        * (honeybee_energy.schedule.ruleset.ScheduleRuleset): The new Honeybee Schedule
    """

    type_limit = schedule_type_limit_by_identifier(_type_limit)

    schedule = ScheduleRuleset.from_constant_value(clean_and_id_ep_string(_name), _value, type_limit)

    schedule.display_name = _name

    return schedule


# def hb_schedule_to_data(_schedule_object):
#     """Get the Honeybee Schedule values as Data, using default inputs"""

#     if not _schedule_object:
#         return None

#     week_start_day = "Sunday"
#     start_date, end_date, timestep = Date(1, 1), Date(12, 31), 1
#     holidays = None

#     return _schedule_object.data_collection(timestep, start_date, end_date, week_start_day, holidays, leap_year=False)
