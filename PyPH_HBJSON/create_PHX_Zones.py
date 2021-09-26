# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions used to build WUFI Zones and WUFI Rooms based on HB-Model inputs"""

import honeybee.room
import PHX.bldg_segment
import PHX.spaces
import PHX.summer_ventilation
import PHX.programs.schedules
import PHX.programs.occupancy
import PHX.appliances
import LBT_Utils.boundary_conditions

# -- Thermal Zones
# ------------------------------------------------------------------------------
def create_PHX_Zone_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.bldg_segment.Zone:
    """Creates a new PHX-Zone from a single Honeybee 'Room'.

    Note: This function does not create the 'PHX-Spaces' within the PHX-Zone. Use
    create_PHX_Zones.add_Spaces_from_HB_room() in order to add Spaces if desired.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee room to use as the source for the new PHX-Zone

    Returns:
    --------
        * (PHX.bldg_segment.Zone): The new PHX-Zone object with Attributes based on the Honeybee Room
    """

    zone = PHX.bldg_segment.Zone()
    zone.n = _hb_room.display_name
    zone.identifier = _hb_room.identifier
    zone.source_zone_identifiers.append(_hb_room.identifier)

    # -- Summer Ventilation Parameters
    zone.summer_ventilation = PHX.summer_ventilation.SummerVent.from_dict(
        _hb_room.user_data.get("phx", {}).get("summ_vent", {})
    )

    # -- ZoneOccupany Parameters
    occ_dict = _hb_room.user_data.get("phx", {}).get("zone_occupancy", {})
    zone.occupancy = PHX.programs.occupancy.ZoneOccupancy.from_dict(occ_dict)

    # -- Add in any Zone-Appliances
    appliance_set_dict = _hb_room.user_data.get("phx", {}).get("zone_appliances", {})
    zone.appliances = PHX.appliances.ApplianceSet.from_dict(appliance_set_dict)

    return zone


def get_host_PHX_Zone(
    _bldg_segment: PHX.bldg_segment.BldgSegment, _hb_room: honeybee.room.Room
) -> PHX.bldg_segment.Zone:
    """Ty and return an existing Zone from the BldgSegment based on the HB Room ID, if it exists.
    If none found by that ID, or no ID input, return a new PHX-Zone based on the HB-Room.
    """

    zone_identifier = (_hb_room.user_data or {}).get("phx", {}).get("zone_id", {}).get("identifier", None)
    zone = _bldg_segment.get_zone_by_identifier(zone_identifier)
    if not zone:
        zone = create_PHX_Zone_from_HB_room(_hb_room)

    return zone


def create_PHX_Spaces_from_HB_room(_hb_room):
    # type: (honeybee.room.Room) -> list[PHX.spaces.Space]
    """Returns a list of new PHX-Spaces based on the Honeybee Room"""

    # --- Get any detailed user-determined Space info on the HB-Room
    user_determined_space_dict = _hb_room.user_data.get("phx", {}).get("spaces", [])

    spaces = []
    if user_determined_space_dict:
        # --- Build new Spaces based on the User-determined detailed inputs
        for space_dict in user_determined_space_dict.values():

            new_phx_space = PHX.spaces.Space.from_dict(space_dict)
            spaces.append(new_phx_space)
    else:
        # --- Build a default space for the zone, if no detailed spaces are provided
        new_phx_space = PHX.spaces.Space()
        new_phx_space.space_number = None
        new_phx_space.space_name = f"{_hb_room.display_name}_room"

        spaces.append(new_phx_space)

    return spaces
