# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to create PHX Materiala, Assembly-Layers, and Construction Assemblies from HB-JSON"""

import honeybee.room
import PHX.bldg_segment
import PHX.project


def get_host_PHX_BldgSegment(
    _project: PHX.project.Project, _hb_room: honeybee.room.Room
) -> PHX.bldg_segment.BldgSegment:
    """Returns a Honybee Room's Host PHX-BldgSegment.

    Will first look for the Honeybee.room.Room.user_data['phx']['bldg_segment'] to
    get a name/id for the PHX-BldgSegment. If name/id is found, will create a new BldgSegment
    with that id if none already exists on the PHX.project.Project object.

    If none is found (this attribute wasn't set by the
    user), will return the PHX.project.Project's default-BldgSegment.

    Arguments:
    ----------
        * _project (PHX.project.Project): The PHX-Project Object.
        * _ hb_room (honeybee.room.Room): The Honeybee Room to use as the source.

    Returns:
    --------
        * (PHX.bldg_segment.BldgSegment): The Honeybee Room's host PHX-BldgSegment.
    """

    var_ident = (
        _hb_room.user_data.get("phx", {}).get("bldg_segment", {}).get("identifier")
    )
    var_id = _hb_room.user_data.get("phx", {}).get("bldg_segment", {}).get("id")
    var_name = _hb_room.user_data.get("phx", {}).get("bldg_segment", {}).get("name")

    if not var_ident:
        host_bldg_segment = PHX.bldg_segment.BldgSegment.default()
    else:
        host_bldg_segment = _project.get_segment_by_identifier(var_ident)

        if not host_bldg_segment:
            host_bldg_segment = PHX.bldg_segment.BldgSegment()
            host_bldg_segment.identifier = var_ident
            host_bldg_segment.id = var_id
            host_bldg_segment.n = var_name

    _project.add_segment(host_bldg_segment)

    return host_bldg_segment
