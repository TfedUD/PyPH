# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to calculate PHIUS Multi-Family (MF) electric demand.

Note: Calculations taken from "PHIUS Multifamily Calculator"  - PHIUS+2015_Multi-Family_Calculator-04_05_16.xlsx
https://www.phius.org/software-resources/wufi-passive-and-other-modeling-tools/calculators-and-protocols , Multifamily-specific
"""

from collections import defaultdict
from collections import namedtuple

import PHX.spaces
import PHX.occupancy

import honeybee.room


class MissingStoriesError(Exception):
    def __init__(self, _msg):
        self.message = _msg
        super(MissingStoriesError, self).__init__(self.message)


def sort_rooms_by_story(_rooms):
    # type: (honeybee.room.Room) -> dict[list[honeybee.room.Room]]
    HB_rooms_by_story = defaultdict(list)

    for room in _rooms:
        if room.story is None:
            msg = (
                'Warning: To use the PHIUS "Floor" method, please assign Honeybee Rooms '
                'to Stories using "HB Set Story" Component. Honeybee Room: {}\n '
                "is missing Story / Level assignment.".format(room.display_name)
            )
            raise MissingStoriesError(msg)
        else:
            HB_rooms_by_story[room.story].append(room)

    return HB_rooms_by_story


def get_story_attributes(_rooms):
    """
    Arguments:
    ----------
        * _rooms (list[honeybee.room.Room]): A list of HB rooms representing a 'Story' of the building

    Returns:
    --------
        * tuple()
    """
    Output = namedtuple("Output", ["num_bedrooms", "num_dwelling_units", "sf_per_unit"])

    total_story_iCFA_m2 = 0
    total_story_num_bedrooms = 0
    total_story_num_dwelling_units = 0
    for room in _rooms:
        # -- Get the iCFA
        for space_dict in room.user_data.get("phx", {}).get("spaces", {}).values():
            sp = PHX.spaces.Space.from_dict(space_dict)
            total_story_iCFA_m2 += sp.floor_area_weighted

        # -- Get units, bedrooms
        zn_occ_dict = room.user_data.get("phx", {}).get("zone_occupancy", {})
        zn_occ = PHX.occupancy.ZoneOccupancy.from_dict(zn_occ_dict)

        total_story_num_bedrooms += zn_occ.num_bedrooms
        total_story_num_dwelling_units += zn_occ.num_dwelling_units
        total_story_iCFA_sf = total_story_iCFA_m2 * 10.7639
        sf_per_unit = total_story_iCFA_sf / total_story_num_dwelling_units

    return Output(total_story_num_bedrooms, total_story_num_dwelling_units, sf_per_unit)


def story_lighting_interior(_sf_per_unit, _num_dwelling_units, _frac_high_efficiency):
    # type: (float, int, float) -> float
    """Returns total story's interior lighting energy usage (kWh/year)"""

    a = 0.2 + 0.8 * (4 - 3 * _frac_high_efficiency) / 3.7
    b = _num_dwelling_units * 455 + 0.8 * _sf_per_unit
    return a * b * 0.8


def story_lighting_exterior(_sf_per_unit, _num_dwelling_units, _frac_high_efficiency):
    # type: (float, int, float) -> float
    """Returns total story's exterior lighting energy usage (kWh/year)"""

    a = 1 - 0.75 * _frac_high_efficiency
    b = _num_dwelling_units * 100 + 0.05 * _sf_per_unit
    return a * b * 0.8


def story_lighting_garage(_num_dwelling_units, _frac_high_efficiency):
    # type: (int, float) -> float
    """Returns total story's garage lighting energy usage (kWh/year)"""

    return _num_dwelling_units * (100 * (1 - _frac_high_efficiency) + 25 * _frac_high_efficiency) * 0.8


def story_mel(_sf_per_unit, _num_dwelling_units, _num_bedrooms):
    # type: (float, int, int) -> float
    """Returns the story's MEL energy usage (kWh/yr)"""

    a = _num_dwelling_units * 413 + 69 * _num_bedrooms + 0.91 * _sf_per_unit
    return a * 0.8
