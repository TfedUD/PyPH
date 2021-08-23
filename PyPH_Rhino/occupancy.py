# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to calculate Space-Level Occupancy attributes """

import PHX.occupancy
import honeybee_energy.schedule.ruleset


def _clean_HB_program_name(_name):
    # type: (str) -> str
    """Cleans the HB name

    ie: "2013::MutiFam::Corridor" --> "Corridor"
    "Corrior_People" --> "Corridor"
    """
    clean = str(_name).split("::")[-1]
    clean = str(clean).replace("_People", "")
    return clean


def _relative_absence_factor(_HB_sched):
    # type: (honeybee_energy.schedule.ruleset.ScheduleRuleset) -> float
    """Return relative absence factor (1=always absent, 0=never absent) based on HB annual schedule"""
    return 1 - (sum(_ for _ in _HB_sched.values()) / len(_HB_sched.values()))


def phx_occupancy_from_hb(_hb_occupancy):
    # type: (honeybee_energy.load.people.People | None) -> PHX.occupancy.SpaceOccupancy
    """Returns a new PHX-SpaceOccupancy based on a Honeybee Occupancy"""

    occ = PHX.occupancy.SpaceOccupancy()
    occ.start_hour = 1
    occ.end_hour = 24
    occ.annual_utilization_days = 365

    if _hb_occupancy:
        occ.name = _clean_HB_program_name(_hb_occupancy.display_name)
        occ.relative_absence = _relative_absence_factor(_hb_occupancy.occupancy_schedule)
        occ.people_per_area = _hb_occupancy.people_per_area
    else:
        occ.name = "Zero_Occupancy"
        occ.relative_absence = 1.0
        occ.people_per_area = 0.0

    return occ
