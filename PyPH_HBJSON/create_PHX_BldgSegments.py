# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to create PHX Materiala, Assembly-Layers, and Construction Assemblies from HB-JSON"""

from honeybee.room import Room
from honeybee.model import Model
from PHX.bldg_segment import BldgSegment, PHIUSCertification
from PHX.project import Project
from PHX.programs.occupancy import BldgSegmentOccupancy
import PHX.climate


def create_PHX_BldgSegment_from_HB_Room(_hb_room: Room) -> BldgSegment:
    """
    Returns a new Building Segment obejct with its attributes set based on the Honyebee Room

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee Room to get the BldgSegment information / attributes from

    Returns:
    --------
        * (PHX.bldg_segment.BldgSegment): The new BldgSegment
    """

    # -- Get the user-input info
    seg_dict = _hb_room.user_data.get("phx", {}).get("bldg_segment_id", {})
    var_ident = seg_dict.get("identifier")
    var_id = seg_dict.get("id")
    var_name = seg_dict.get("name")

    # -- Build the new BldgSegment
    host_bldg_segment = BldgSegment()
    host_bldg_segment.identifier = var_ident
    host_bldg_segment.id = var_id
    host_bldg_segment.name = var_name

    # -- Set the Segment Occupancy
    occupancy_dict = _hb_room.user_data.get("phx", {}).get("segment_occupancy", {})
    if occupancy_dict:
        occ_obj = BldgSegmentOccupancy.from_dict(occupancy_dict)
        host_bldg_segment.occupancy = occ_obj

    # -- Set Passive House Params
    ph_cert_dict = _hb_room.user_data.get("phx", {}).get("ph_certification", {})
    if ph_cert_dict:
        cert_obj = PHIUSCertification.from_dict(ph_cert_dict)
        host_bldg_segment.PHIUS_certification = cert_obj

    return host_bldg_segment


def get_host_PHX_BldgSegment(_project: Project, _hb_room: Room) -> BldgSegment:
    """Returns a Honybee Room's Host PHX-BldgSegment.

    Will first look for the Honeybee.room.Room.user_data['phx']['bldg_segment'] to
    get a name/id for the PHX-BldgSegment. If name/id is found, will create a new BldgSegment
    with that id if none already exists on the PHX.project.Project object.

    If none is found (meaning: this attribute wasn't set by the
    user), will return the PHX.project.Project's default-BldgSegment.

    Arguments:
    ----------
        * _project (PHX.project.Project): The PHX-Project Object.
        * _ hb_room (honeybee.room.Room): The Honeybee Room to use as the source.

    Returns:
    --------
        * (PHX.bldg_segment.BldgSegment): The Honeybee Room's host PHX-BldgSegment.
    """

    # -- Try and get any user-defined BldgSegment info that has been specified
    seg_dict = _hb_room.user_data.get("phx", {}).get("bldg_segment_id", {})

    if not seg_dict:
        # -- Use the default BldgSegment if, none is provided by the user
        host_bldg_segment = BldgSegment.default()
    else:
        # -- Check if the Segment already exists on the Project.
        host_bldg_segment = _project.get_segment_by_identifier(seg_dict.get("identifier"))
        if not host_bldg_segment:
            # -- If the Segment does not already exist in the Project, build a new one
            host_bldg_segment = create_PHX_BldgSegment_from_HB_Room(_hb_room)

    _project.add_segment(host_bldg_segment)

    return host_bldg_segment


def set_segment_climate_from_hb_model(_hb_model: Model, _phx_seg: BldgSegment) -> BldgSegment:
    """Sets the BuildingSegment's Climate from HB Model user_data.

    Arguments:
    ----------
        * _hb_model (honeybee.model.Model): The Honeybee Model to try and read the
            climate data from.
        * _phx_seg (PHX.bldg_segment.BldgSegment): The Building Segment to set the
            Climate data for.

    Returns:
    --------
        * (PHX.bldg_segment.BldgSegment): The Building Segmeng with its Climate set.
    """

    phx_climate_dict = (_hb_model.user_data or {}).get("phx", {}).get("climate", {})

    if phx_climate_dict:
        _phx_seg.climate = PHX.climate.Climate.from_dict(phx_climate_dict)

    return _phx_seg


def filter_out_Surface_Exposure(_phx_seg: BldgSegment) -> BldgSegment:
    """Remove any Component from the BldgSegment which has a 'Surface' exposure type (-4).
        ie: Any component surface where Honeybee assigned a 'Surface<->Surface' adjacency.
        This is done since WUFI does NOT want interior zone<->zone surfaces. If interior surfaces
        are left in the model then when WUFI calculates the Peak Load it will assume
        heat transfer accross all of those surfaces, which will give really wierd restults.

    Arugments:
    ----------
        * _phx_seg (PHX.bldg_segment.BldgSegment): The Building Segement to filter
            out the components for.

    Returns:
    --------
        * (PHX.bldg_segment.BldgSegment): The Building Segment with the component
            surfaces removed.
    """

    _phx_seg.components = [_ for _ in _phx_seg.components if _.ext_exposure_zone_id != -4]

    return _phx_seg
