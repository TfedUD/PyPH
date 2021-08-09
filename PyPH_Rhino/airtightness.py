# -*- coding: utf-8 -*-
"""Envelope Airtightness GH-Component functions for calculating airtightness using Vn50"""

import PHX.spaces
import math


class NoPHXSpaceError(Exception):
    def __init__(self, _hb_rm_nm, _d):
        self.message = (
            'Error: No PHX Spaces found on Honeybee Room: "{}".\n'
            'Instead got: "{}".\n'
            "Please be sure to add PHX Spaces to the Honeybee Room before using this component".format(
                _hb_rm_nm, _d
            )
        )
        super(NoPHXSpaceError, self).__init__(self.message)


def preview_infiltration_calc(_hb_room, PHX_space_vn50, room_infil_airflow, _pressure):
    """Print out inputs and results to GH Component"""

    print("{} HB-Room: {}{}".format("- " * 15, _hb_room.display_name, "- " * 15))
    print("INPUTS:")
    print("  > HB-Room PHX Space Volumes (Vn50) = {:.2f} m3".format(PHX_space_vn50))
    print("  > HB-Room E+ Volume (Gross) = {:.1f} m3".format(_hb_room.volume))
    print("  > HB-Room E+ Floor Area (Gross) = {:.1f} m2".format(_hb_room.floor_area))
    print(
        "  > HB-Room E+ Exposed Surface Area = {:.1f} m2".format(_hb_room.exposed_area)
    )
    print("RESULT:")
    print(
        "  > HB-Room New Total Infiltration Flowrate: {:.2f} m3/hr ({:.4f} m3/s) @ {}Pa".format(
            room_infil_airflow * 60 * 60, room_infil_airflow, _pressure
        )
    )


def calc_hb_room_infiltration_rate(_hb_room, _n50, _q50, _pressure, _preview=False):

    # - Probably can just get this info from the flat dict? No need to rebuild the object?
    spaces_dict = _hb_room.user_data.get("phx", {}).get("spaces")
    if not spaces_dict:
        raise NoPHXSpaceError(_hb_room.display_name, spaces_dict)

    PHX_space_vn50 = sum(float(_.get("volume")) for _ in spaces_dict.values())

    if _n50:
        room_infil_airflow = (PHX_space_vn50 * _n50) / 3600  # m3/s
    elif _q50:
        room_infil_airflow = _hb_room.exposed_area * _q50 / 3600
    else:
        room_infil_airflow = (
            _hb_room.exposed_area
            * _hb_room.properties.energy.infiltration.flow_per_exterior_area
            / 3600
        )

    if _preview:
        preview_infiltration_calc(
            _hb_room, PHX_space_vn50, room_infil_airflow, _pressure
        )

    return room_infil_airflow


def calc_standard_flow_rate(_hb_room_infilt_rate, _pressure=50.0):
    """Flow Rate incorporating Blower Pressure
    This equation comes from Honeybee. The HB Component uses a standard pressure
    at rest of 4 Pascals.

    """

    normal_avg_pressure = 4.0  # Pa
    factor = math.pow((_pressure / normal_avg_pressure), 0.63)
    standardFlowRate = _hb_room_infilt_rate / factor  # m3/s

    return standardFlowRate
