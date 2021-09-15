# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for handling Loads, pulled from Honeybee 'ApplyLoadVals' Grasshopper component"""

from honeybee.typing import clean_and_id_ep_string
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.lib.scheduletypelimits import schedule_type_limit_by_identifier


def calc_utilization_factor(_HB_sched):
    # type: (ScheduleRuleset) -> float
    """Return annual utilization factor based on HB annual schedule.
    (0=always absent, 1=always present)

    Argumemnts:
    ----------
        * _HB_sched (honeybee_energy.schedule.ruleset.ScheduleRuleset)
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
