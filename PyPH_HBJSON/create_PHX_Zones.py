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
import loggers.HBJSON_loggers


@loggers.HBJSON_loggers.log_function_info
def create_PHX_Zone_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.bldg_segment.Zone:
    """Creates a new PHX-Zone from a single Honeybee 'Room'.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee room to use as the source for the new PHX-Zone

    Returns:
    --------
        * (PHX.bldg_segment.Zone): The new PHX-Zone object with Attributes based on the Honeybee Room
    """

    zone = PHX.bldg_segment.Zone()
    zone.name = _hb_room.display_name
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
    zone.appliance_set = PHX.appliances.ApplianceSet.from_dict(appliance_set_dict)

    return zone


@loggers.HBJSON_loggers.log_function_info
def get_host_PHX_Zone(
    _bldg_segment: PHX.bldg_segment.BldgSegment, _hb_room: honeybee.room.Room
) -> PHX.bldg_segment.Zone:
    """Ty and return an existing Zone from the BldgSegment based on the HB Room ID, if it exists.
    If none found by that ID, or no ID input, return a new PHX-Zone based on the HB-Room.
    """

    # First, see if there is any user-defined Zone id
    zone_identifier = (_hb_room.user_data or {}).get("phx", {}).get("zone_id", {}).get("identifier", None)
    zone = _bldg_segment.get_zone_by_identifier(zone_identifier)
    if not zone:
        # -- If not, try and use the Room's identifier to find any existing Zone
        zone = _bldg_segment.get_zone_by_identifier(_hb_room.identifier)
        if not zone:
            # -- If it still isn't found, make a new one
            zone = create_PHX_Zone_from_HB_room(_hb_room)

    return zone
