# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Rhino/Grasshopper Envelope Airtightness functions for calculating airtightness using Vn50"""

import honeybee.face
import LBT_Utils.boundary_conditions


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


def preview_infiltration_calc(
    _hb_room, PHX_space_vn50, room_infil_airflow, _pressure, _phx_exposed_area
):
    """Print out inputs and results to GH Component"""

    print("{} HB-Room: {}{}".format("- " * 15, _hb_room.display_name, "- " * 15))
    print("INPUTS:")
    print("  > HB-Room PHX Space Volumes (Vn50) = {:.2f} m3".format(PHX_space_vn50))
    print("  > HB-Room E+ Volume (Gross) = {:.1f} m3".format(_hb_room.volume))
    print("  > HB-Room E+ Floor Area (Gross) = {:.1f} m2".format(_hb_room.floor_area))
    print(
        "  > HB-Room E+ Exposed Surface Area (no ground) = {:.1f} m2".format(
            _hb_room.exposed_area
        )
    )
    print(
        "  > HB-Room PHX Exposed Surface Area (with ground) = {:.1f} m2".format(
            _phx_exposed_area
        )
    )
    print(
        "  > HB-Room Specific Infiltration Flowrate: {:.2f} m3/hr-m2 ({:.4f} m3/s-m2) @ {}Pa".format(
            (room_infil_airflow / _phx_exposed_area) * 3600,
            (room_infil_airflow / _phx_exposed_area),
            _pressure,
        )
    )
    print("RESULT:")
    print(
        "  > HB-Room Absolute Infiltration Flowrate:\n"
        "  >        {:.2f}m3/h-m2 x {:.2f}m2 = {:.2f} m3/hr ({:.4f} m3/s) @ {}Pa".format(
            (room_infil_airflow / _phx_exposed_area) * 3600,
            _phx_exposed_area,
            room_infil_airflow * 3600,
            room_infil_airflow,
            _pressure,
        )
    )


def calc_hb_room_infiltration_m3s(_hb_room, _n50, _q50, _pressure, _preview=False):
    # type: (honeybee.room.Room, float, float, float, bool) -> float
    """Returns the Infiltration flow rate (m3/s) at the specified pressure differential

    Note: for q50 values: PHIUS exterior 'exposed surfaces' includes the ground, while
    the normal Honeybee "room.exposed_area" property does NOT.

    Note: for n50, PHI and PHIUS use net-interior volume, while Honeybee uses gross volume.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee Room.
        * _n50 (float | None): Volumetric leakage rate at test-pressure (ach).
        * _q50 (float | None): Envelope specific leakage area at test-pressure (m3/s-m2).
        * _pressure (float): Blower Door test pressure (Pa).
        * _preview (bool): Show Preivew?

    Returns:
    --------
        * (float): The honeybee room's infiltration airflow (m3/s) at test-pressure.
    """

    # - Probably can just get this info from the flat dict? No need to rebuild the object?
    spaces_dict = _hb_room.user_data.get("phx", {}).get("spaces")
    if not spaces_dict:
        raise NoPHXSpaceError(_hb_room.display_name, spaces_dict)

    PHX_space_vn50 = sum(float(_.get("volume")) for _ in spaces_dict.values())
    PHX_exposed_area = LBT_Utils.boundary_conditions.hb_room_PHX_exposed_area(_hb_room)

    if _n50:
        room_infil_airflow = (PHX_space_vn50 * _n50) / 3600
    elif _q50:
        room_infil_airflow = PHX_exposed_area * _q50
    else:
        room_infil_airflow = (
            PHX_exposed_area
            * _hb_room.properties.energy.infiltration.flow_per_exterior_area
        )

    if _preview:
        preview_infiltration_calc(
            _hb_room, PHX_space_vn50, room_infil_airflow, _pressure, PHX_exposed_area
        )

    return room_infil_airflow
