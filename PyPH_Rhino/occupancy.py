# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to calculate Space-Level Occupancy attributes """

import PHX.occupancy
import PHX.utilization_patterns
import honeybee_energy.schedule.ruleset
import LBT_Utils.program
import LBT_Utils.hb_schedules


def phx_occupancy_from_hb(_hb_occupancy):
    # type: (honeybee_energy.load.people.People | None) -> PHX.occupancy.SpaceOccupancy
    """Returns a new PHX-SpaceOccupancy based on a Honeybee Occupancy"""

    occ = PHX.occupancy.SpaceOccupancy()

    if _hb_occupancy:
        occ.identifier = _hb_occupancy.identifier
        occ.name = LBT_Utils.program.clean_HB_program_name(_hb_occupancy.display_name)
        occ.people_per_area = _hb_occupancy.people_per_area

        # Utilization Rates
        occ.utilization = PHX.utilization_patterns.UtilPat_Occupancy.default()
        annual_util = LBT_Utils.hb_schedules.calc_utilization_factor(_hb_occupancy.occupancy_schedule)
        occ.utilization.annual_utilization_factor = annual_util
    else:
        occ.name = "Zero_Occupancy"
        occ.utilization.annual_utilization_factor = 1.0
        occ.people_per_area = 0.0

    return occ
