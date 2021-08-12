# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to create PHX Materiala, Assembly-Layers, and Construction Assemblies from HB-JSON"""

import honeybee.room
import PHX.bldg_segment
import PHX.project
import PHX.occupancy


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

    seg_dict = _hb_room.user_data.get("phx", {}).get("bldg_segment_id", {})
    if not seg_dict:
        # -- Use the default Segment if none is provided
        host_bldg_segment = PHX.bldg_segment.BldgSegment.default()
    else:
        # -- Build a new Segment if there is data for one.
        var_ident = seg_dict.get("identifier")
        var_id = seg_dict.get("id")
        var_name = seg_dict.get("name")

        # -- Check if the Segment already exists on the Project.
        # -- If it does not exist, build a new one
        host_bldg_segment = _project.get_segment_by_identifier(var_ident)
        if not host_bldg_segment:
            host_bldg_segment = PHX.bldg_segment.BldgSegment()
            host_bldg_segment.identifier = var_ident
            host_bldg_segment.id = var_id
            host_bldg_segment.n = var_name

            # -- Occupancy
            occupancy_dict = _hb_room.user_data.get("phx", {}).get("occupancy", {})
            if occupancy_dict:
                occ_obj = PHX.occupancy.BldgSegmentOccupancy.from_dict(occupancy_dict)
                host_bldg_segment.occupancy = occ_obj

            # -- Passive House Params
            ph_cert_dict = _hb_room.user_data.get("phx", {}).get("ph_certification", {})
            if ph_cert_dict:
                cert_obj = PHX.bldg_segment.PHIUSCertification.from_dict(ph_cert_dict)
                host_bldg_segment.PHIUS_certification = cert_obj

    _project.add_segment(host_bldg_segment)

    return host_bldg_segment
