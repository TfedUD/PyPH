# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to create PHX-Floors, PHX-Volumes and PHX-Spaces from Rhino inputs"""

from collections import defaultdict

import PHX.spaces
import space_io
import space_floors
import space_volumes
import gh_io


def build_floors(IGH, _floor_surfaces, _input_node_name, _HB_rooms):
    # type: (gh_io.IGH, list, str, list) -> tuple[ dict, list]
    """Creates new Floor objects from user-inputs

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _floor_surfaces (list): The input items
        * _input_node_name (str): The name (string) of the GH Component input node to read
        * _HB_rooms (list[honeybee.rooms])

    Returns:
    --------
        * (dict): The dict of all the Floors, organized by HB Room
        * (list[Rhino.Geometry.Brep]): A list of the Breps for all the FloorSegments
    """

    if not _HB_rooms:
        return {}

    input_floor_surfaces = space_io.handle_input_geometry(IGH, _floor_surfaces, _input_node_name)
    hb_room_dicts = space_floors.sort_floor_surfaces_by_hb_room(input_floor_surfaces, _HB_rooms)
    hb_room_dicts = space_floors.add_default_floor_surfaces(IGH, hb_room_dicts)
    hb_room_dicts = space_floors.convert_inputs_to_FloorSements(hb_room_dicts)

    hb_room_dicts = space_floors.group_FloorSegments_by_room_name(hb_room_dicts)
    floors_dict = space_floors.create_Floors_from_FloorSegments(IGH, hb_room_dicts)

    # --- Get Floor Geometry for Preview
    floor_surface_breps_ = []
    for v in floors_dict.values():
        for floors in v["Floors"].values():
            for floor in floors:
                for face in floor.geometry:
                    c = IGH.convert_to_rhino_geom(face)
                    floor_surface_breps_.extend(c)

    return floors_dict, floor_surface_breps_


def build_volumes(IGH, _floors_dict, _space_geometry, _input_node_name):
    # type: (gh_io.IGH, dict, list, str) -> tuple[ dict, list ]
    """Creates new Floor objects from user-inputs

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _floors_dict (dict): The input items to build volumes from
        * _space_geometry (list):
        * _input_node_name (str): The name (string) of the GH Component input node to read

    Returns:
    --------
        * (dict): The dict of all the Floors, organized by HB Room
        * (list[Rhino.Geometry.Brep]): A list of the Breps for all the Space Geometry
    """

    input_space_geometry = space_io.handle_input_geometry(IGH, _space_geometry, _input_node_name)
    input_space_geometry_dict = {id(v): v for v in input_space_geometry}
    volumes = space_volumes.create_volumes(IGH, _floors_dict, input_space_geometry_dict)

    # -- Get geometry for preview
    volume_geometry_breps_ = []
    for v in volumes.values():
        for volume in v["Volumes"]:
            for _ in volume.volume_geometry:
                v = IGH.convert_to_rhino_geom(_)
                volume_geometry_breps_.extend(v)

    return volumes, volume_geometry_breps_


def build_spaces(_volume_dict):
    # type: (dict) -> dict
    """Creates a new Space based on the input Volumes

    Arguments:
    ---------
        * _volume_dict (dict): The Volumes to turn into Spaces

    Returns:
    -------
        * (dict): A dict of the new Spaces, organized by HB-Room
    """

    # --- Group the volumes by Space Name/Number
    for hb_room_dict in _volume_dict.values():
        hb_room_dict["Spaces"] = []
        volume_groups_dict = defaultdict(list)

        for volume in hb_room_dict["Volumes"]:
            volume_groups_dict[volume.display_name].append(volume)

        # --- Create the new Space for each Volume group
        for volume_group in volume_groups_dict.values():
            new_space = PHX.spaces.Space()
            for volume in volume_group:
                new_space.add_new_volume(volume)

            hb_room_dict["Spaces"].append(new_space)

        del hb_room_dict["Volumes"]

    return _volume_dict
