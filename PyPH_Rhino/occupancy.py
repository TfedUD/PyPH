# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to calculate Space-Level Occupancy attributes """

import PHX.programs.occupancy
import PHX.programs.schedules
import honeybee_energy.schedule.ruleset
import LBT_Utils.program
import LBT_Utils.hb_schedules


def phx_occupancy_from_hb(_hb_occupancy, _name=None):
    # type: (honeybee_energy.load.people.People | None, str) -> PHX.programs.occupancy.RoomOccupancy
    """Returns a new PHX-RoomOccupancy based on a Honeybee Occupancy"""

    occ = PHX.programs.occupancy.RoomOccupancy()

    if _hb_occupancy:

        occ.name = "OCC_{}".format(LBT_Utils.program.clean_HB_program_name(_hb_occupancy.display_name))

        # -- Loads
        occ.loads.people_per_area = _hb_occupancy.people_per_area

        # -- Schedules
        occ.schedule = PHX.programs.schedules.Schedule_Occupancy.default()
        annual_util = LBT_Utils.hb_schedules.calc_utilization_factor(_hb_occupancy.occupancy_schedule)
        occ.schedule.annual_utilization_factor = annual_util

        # -- Try and set the detaled Schedule data, if it is supplied
        ud = _hb_occupancy.occupancy_schedule.user_data or {}
        ud_sched_dict = ud.get("phx", {}).get("schedule", None)
        if ud_sched_dict:
            occ.schedule.name = occ.name
            occ.schedule.start_hour = ud_sched_dict.get("start_hour")
            occ.schedule.end_hour = ud_sched_dict.get("end_hour")
            occ.schedule.annual_utilization_days = ud_sched_dict.get("annual_utilization_days")
            occ.schedule.relative_utilization_factor = ud_sched_dict.get("relative_utilization_factor")
    else:
        occ.name = "OCC_{}".format(LBT_Utils.program.clean_HB_program_name(_name) or "ZERO")
        occ.schedule.annual_utilization_factor = 1.0
        occ.loads.people_per_area = 0.0

    return occ
