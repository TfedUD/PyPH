# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to calculate Space-Level Occupancy attributes """

import PHX.occupancy
import PHX.schedules
import honeybee_energy.schedule.ruleset
import LBT_Utils.program
import LBT_Utils.hb_schedules


def phx_occupancy_from_hb(_hb_occupancy, _name=None):
    # type: (honeybee_energy.load.people.People | None, str) -> PHX.occupancy.SpaceOccupancy
    """Returns a new PHX-SpaceOccupancy based on a Honeybee Occupancy"""

    occ = PHX.occupancy.SpaceOccupancy()

    if _hb_occupancy:
        # occ.identifier = _hb_occupancy.identifier
        occ.name = "OCC_{}".format(LBT_Utils.program.clean_HB_program_name(_hb_occupancy.display_name))
        occ.loads.people_per_area = _hb_occupancy.people_per_area

        # Utilization Rates
        occ.schedule = PHX.schedules.Schedule_Occupancy.default()
        annual_util = LBT_Utils.hb_schedules.calc_utilization_factor(_hb_occupancy.occupancy_schedule)
        occ.schedule.annual_utilization_factor = annual_util
    else:
        occ.name = "OCC_{}".format(LBT_Utils.program.clean_HB_program_name(_name) or "ZERO")
        occ.schedule.annual_utilization_factor = 1.0
        occ.loads.people_per_area = 0.0

    return occ


def hb_occupancy_from_phx(_PHX_Occupancy):
    pass
