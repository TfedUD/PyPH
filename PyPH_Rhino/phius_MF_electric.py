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
    """Returns a dict of Honeybee rooms, organized by 'Story' (level)."""

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


def get_room_attributes(_rooms):
    # type: (honeybee.room.Room) -> tuple
    """
    Arguments:
    ----------
        * _rooms (list[honeybee.room.Room]): A list of HB rooms representing a 'Story' of the building

    Returns:
    --------
        * tuple():
            - num_bedrooms:
            - num_dwelling_units:
            - m2_per_unit:
            - total_iCFA:
    """
    Output = namedtuple("Output", ["num_bedrooms", "num_dwelling_units", "m2_per_unit", "total_iCFA"])

    if not isinstance(_rooms, list):
        _rooms = [_rooms]

    total_story_iCFA_m2 = 0
    total_story_num_bedrooms = 0
    total_story_num_dwelling_units = 0
    for room in _rooms:
        if not room:
            continue

        # -- Get the iCFA
        for space_dict in room.user_data.get("phx", {}).get("spaces", {}).values():
            sp = PHX.spaces.Space.from_dict(space_dict)
            total_story_iCFA_m2 += sp.floor_area_weighted

        # -- Get units, bedrooms
        zn_occ_dict = room.user_data.get("phx", {}).get("zone_occupancy", {})
        zn_occ = PHX.occupancy.ZoneOccupancy.from_dict(zn_occ_dict)

        total_story_num_bedrooms += zn_occ.num_bedrooms
        total_story_num_dwelling_units += zn_occ.num_dwelling_units

    try:
        sf_per_unit = total_story_iCFA_m2 / total_story_num_dwelling_units
    except ZeroDivisionError:
        sf_per_unit = 0

    return Output(total_story_num_bedrooms, total_story_num_dwelling_units, sf_per_unit, total_story_iCFA_m2)


def story_lighting_interior(_m2_per_unit, _num_dwelling_units, _frac_high_efficiency):
    # type: (float, int, float) -> float
    """Returns total story's interior lighting energy usage (kWh/year)"""

    sf_per_unit = _m2_per_unit * 10.7639
    a = 0.2 + 0.8 * (4 - 3 * _frac_high_efficiency) / 3.7
    b = _num_dwelling_units * 455 + 0.8 * sf_per_unit
    return a * b * 0.8


def story_lighting_exterior(_m2_per_unit, _num_dwelling_units, _frac_high_efficiency):
    # type: (float, int, float) -> float
    """Returns total story's exterior lighting energy usage (kWh/year)"""

    sf_per_unit = _m2_per_unit * 10.7639
    a = 1 - 0.75 * _frac_high_efficiency
    b = _num_dwelling_units * 100 + 0.05 * sf_per_unit
    return a * b * 0.8


def story_lighting_garage(_num_dwelling_units, _frac_high_efficiency):
    # type: (int, float) -> float
    """Returns total story's garage lighting energy usage (kWh/year)"""

    return _num_dwelling_units * (100 * (1 - _frac_high_efficiency) + 25 * _frac_high_efficiency) * 0.8


def story_mel(_m2_per_unit, _num_dwelling_units, _num_bedrooms):
    # type: (float, int, int) -> float
    """Returns the story's MEL energy usage (kWh/yr)"""
    sf_per_unit = _m2_per_unit * 10.7639

    a = _num_dwelling_units * 413 + 69 * _num_bedrooms + 0.91 * sf_per_unit
    return a * 0.8


def hb_lighting_values(_hb_room):
    # type: (honeybee.room.Room) -> tuple
    """Return tuple with Honeybee Room's Lighting values.

    Returns:
    --------
        * namedtuple:
            - annual_util_frac (float):
            - util_day_per_yr (int):
            - daily_operating_hrs (float):
            - w_sf (float):
    """

    Output = namedtuple("Output", ["annual_util_frac", "util_day_per_yr", "daily_operating_hrs", "w_sf"])

    annual_utilization_fraction_lighting = sum(_hb_room.properties.energy.lighting.schedule.values())

    return Output(
        annual_utilization_fraction_lighting,
        365,
        (annual_utilization_fraction_lighting / 8760) * 24,
        _hb_room.properties.energy.lighting.watts_per_area / 10.7639,
    )


def hb_mel_values(_hb_room):
    # type: (honeybee.room.Room) -> tuple
    """Return tuple with Honeybee Room's Electric Equipment values.

    Returns:
    --------
        * namedtuple:
            - annual_util_frac (float):
            - kWh_sf_yr (float):
    """

    Output = namedtuple(
        "Output",
        [
            "annual_util_frac",
            "kWh_sf_yr",
        ],
    )

    annual_utilization_fraction_equipment = sum(_hb_room.properties.energy.electric_equipment.schedule.values())
    W_per_sf_equipment = _hb_room.properties.energy.electric_equipment.watts_per_area / 10.7639

    return Output(
        annual_utilization_fraction_equipment,
        (W_per_sf_equipment * annual_utilization_fraction_equipment) / 1000,
    )


def annual_lighting_and_mel(_hb_room, _lighting, _mel):
    # type: (honeybee.room.Room, tuple, tuple) -> tuple
    """Return tuple with Honeybee Room's annual lighting and MEL energy consumption in kWh

    Returns:
    --------
        * namedtuple:
            - spaces (list):
            - lighting_annual_kWh (float):
            - mel_annual_kWh (float):
    """

    Output = namedtuple("Output", ["spaces", "lighting_annual_kWh", "mel_annual_kWh"])

    room_lighting_kwh = 0
    room_mel_kwh = 0
    spaces = []

    space_dict = _hb_room.user_data.get("phx", {}).get("spaces", {})
    for _ in space_dict.values():
        new_space = PHX.spaces.Space.from_dict(_)

        # -- For PHIUS MF Spreadsheet
        spaces.append(
            "{},{},{},{}".format(
                new_space.display_name,
                _hb_room.properties.energy.program_type.display_name,
                "",
                new_space.floor_area_weighted * 10.7639,
            )
        )

        room_lighting_kwh += (
            new_space.floor_area_weighted
            * _lighting.annual_util_frac
            * _hb_room.properties.energy.lighting.watts_per_area
        ) / 1000
        room_mel_kwh += (
            new_space.floor_area_weighted
            * _mel.annual_util_frac
            * _hb_room.properties.energy.electric_equipment.watts_per_area
        ) / 1000

    return Output(spaces, room_lighting_kwh, room_mel_kwh)
