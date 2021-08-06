# -*- coding: utf-8 -*-
"""Functions to create new FloorSegments and Floors based on Rhino Geometry input"""

from collections import defaultdict
import PHX.spaces
import gh_io


class VentilationInputError(Exception):
    def __init__(self, _flr_name, _in):
        self.message = (
            '\nError: Ventilation input for FloorSegment: "{}" '
            'should be a number. Got: "{}"\n'.format(
                _flr_name, self.get_error_item(_in)
            )
        )
        super(VentilationInputError, self).__init__(self.message)

    def get_error_item(self, _in):
        return str(str(_in.message).split(":")[-1]).lstrip().rstrip()


def sort_floor_surfaces_by_hb_room(_floor_surfaces, _hb_rooms):
    # type: (list, list) -> dict
    """Sorts the floor surfaces based on which HB Room they are 'in'

    Uses the HB Room's 'is_point_inside()' method and tests against each floor surface's
    centroid. So note that the entire surface might not be 'in' the room - just
    the centroid.

    Arguments:
    ----------
        * _floor_surfaces ():
        * _hb_rooms ():

    Returns:
    --------
        * (dict) : { hb_room_identifier_1:
                        {
                            'hb_room': HB_Room_1,
                            'floor_surfaces': { 590:srfc1_dict, 591:srfc2_dict, ...}
                        },
                    hb_room_identifier_2:
                        {
                            ...
                        },
                    ...
                    }
    """
    # -- Convert the list to a dict so can remove items during iteration (trying to help speed up)
    _floor_surfaces_dict = {id(srfc): srfc for srfc in _floor_surfaces}

    rooms = {}
    for room in _hb_rooms:
        rooms[room.identifier] = {"hb_room": room, "floor_surfaces": {}}
        for k, v in _floor_surfaces_dict.items():
            for face in v["Geometry"]:
                if room.geometry.is_point_inside(face.centroid):
                    rooms[room.identifier]["floor_surfaces"][k] = v
                    del _floor_surfaces_dict[k]  # -- to help speed up later tests

    # -- If any are left in the bin, throw Exception
    if _floor_surfaces_dict:
        for _ in _floor_surfaces_dict.values():
            raise Exception(
                "Error: Cannot find a host Honeybee room for floor"
                'surface: "{}"?\nMake sure it is inside a HB Room.'.format(
                    _["Object Name"]
                )
            )

    return rooms


def add_default_floor_surfaces(IGH, _room_dicts):
    # type: (gh_io.IGH, dict) -> dict
    """If no user-input floor surfaces are found for a HB Room, create a floor using inset

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _room_dicts (dict): The room dicts to operate on

    Returns:
    --------
        * (dict): The room dicts, modified with the new floor surfaces added
    """

    def _get_hb_room_floor_surfaces(_hb_room):
        """Return a list of only the 'Floor' surfaces in a Honeybee room"""
        floors = []
        for face in _hb_room.faces:
            if "FLOOR" in str(face.type).upper():
                floors.append(face)

        if not floors:
            raise Exception(
                'Error: No Floor found on Honeybee Room: ""'.format(
                    _hb_room.display_name
                )
            )

        return floors

    for room in _room_dicts.values():
        if not room["floor_surfaces"]:
            hb_floor_surfaces = _get_hb_room_floor_surfaces(room["hb_room"])

            new_floors = []
            for srfc in hb_floor_surfaces:
                inset_rh_srfc = IGH.inset_LBT_face(srfc, 0.1)
                try:
                    for _ in inset_rh_srfc:
                        new_floors.extend(_)
                except:
                    new_floors.extend(inset_rh_srfc)

            room["floor_surfaces"] = {
                id(new_floors): {"Object Name": None, "Geometry": new_floors}
            }

    return _room_dicts


def convert_inputs_to_FloorSements(_room_dicts):
    # type: (dict) -> dict
    """Convert the user-input dicts and floor surfaces into FloorSegment objects

    Arguments:
    ----------
        * _room_dicts (dict): The room-dicts with all the user-input values

    Returns:
    --------
        * (dict): The same room dicts, but with all the user-input converted to FloorSegment objects
    """

    for room_identifier, room_dict in _room_dicts.items():
        for k, input_floor_surface_dict in room_dict["floor_surfaces"].items():

            new_floor_seg = PHX.spaces.FloorSegment()

            new_floor_seg.weighting_factor = input_floor_surface_dict.get(
                "TFA_Factor", 1.0
            )
            new_floor_seg.space_name = input_floor_surface_dict.get("Object Name")
            new_floor_seg.space_number = input_floor_surface_dict.get("Room_Number")

            new_floor_seg.non_res_lighting = input_floor_surface_dict.get("lighting")
            new_floor_seg.non_res_motion = input_floor_surface_dict.get("motion")
            new_floor_seg.non_res_usage = input_floor_surface_dict.get("useType")

            try:
                new_floor_seg.ventilation.airflows.supply = float(
                    input_floor_surface_dict.get("V_sup", 0.0)
                )
                new_floor_seg.ventilation.airflows.extract = float(
                    input_floor_surface_dict.get("V_eta", 0.0)
                )
                new_floor_seg.ventilation.airflows.transfer = float(
                    input_floor_surface_dict.get("V_trans", 0.0)
                )
            except ValueError as e:
                raise VentilationInputError(new_floor_seg.display_name, e)

            new_floor_seg.geometry = input_floor_surface_dict.get("Geometry")
            new_floor_seg.host_zone_identifier = room_identifier

            new_floor_seg.floor_area_gross = sum(
                float(geom.area) for geom in new_floor_seg.geometry
            )

            room_dict["floor_surfaces"][k] = new_floor_seg

    return _room_dicts


def group_FloorSegments_by_room_name(_room_dicts):
    # type: (dict) -> dict
    """Sort / Combine User-Input FloorSegments based on their Object-Name & Room-Number

    Arguments:
    ----------
        * _room_dicts (dict): The room dictionaries to look at

    Returns:
    --------
        * (dict): The room dict, with floor surfaces combined based on room name / number
    """

    for room_dict in _room_dicts.values():
        room_dict["FloorSegments"] = {}
        for v in room_dict["floor_surfaces"].values():

            if v.display_name in room_dict["FloorSegments"]:
                room_dict["FloorSegments"][v.display_name].append(v)
            else:
                room_dict["FloorSegments"][v.display_name] = [v]

        del room_dict["floor_surfaces"]

    return _room_dicts


def find_neighbors(IGH, _floor_segment_list):
    # type: (gh_io.IGH, list) -> dict
    """See if any FloorSegments in the inut list are 'neighbors.' Returns a dict
    of the FloorSegments, sorted by 'neighbor-group.'

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _floor_segment_list (list[FloorSegments])

    Returns:
    --------
        * (dict): ie - {10947: set(FloorSegment_1, FloorSegment_2, ...), 10948: set(...), ... }
    """
    neighbor_groups = defaultdict(set)

    # -- If its just a single FloorSegment
    if len(_floor_segment_list) == 1:
        neighbor_groups[id(_floor_segment_list[0])].add(id(_floor_segment_list[0]))

    # -- If its a group of FloorSegments, see if any can be merged
    for floor_seg_a in _floor_segment_list:
        for floor_seg_b in _floor_segment_list:
            if floor_seg_a == floor_seg_b:
                continue
            input_geometry = [floor_seg_a.geometry, floor_seg_b.geometry]

            merge_result = IGH.merge_Face3D(input_geometry)

            if len(merge_result) < len(input_geometry):
                # Merge worked, so record the neighbor group in the list
                for _k, _v in neighbor_groups.items():
                    if id(floor_seg_a) in _v or id(floor_seg_b) in _v:
                        neighbor_groups[_k].add(id(floor_seg_a))
                        neighbor_groups[_k].add(id(floor_seg_b))
                        break
                else:
                    neighbor_groups[id(floor_seg_a)].add(id(floor_seg_a))
                    neighbor_groups[id(floor_seg_a)].add(id(floor_seg_b))

    # -- If any FloorSegment groups can't be merged at all
    for floor_seg in _floor_segment_list:
        for gr in neighbor_groups.values():
            if id(floor_seg) in gr:
                break
        else:
            neighbor_groups[id(floor_seg)].add(id(floor_seg))

    return neighbor_groups


def sort_FloorSegments_by_neighbor(IGH, _floor_segment_list):
    # type: (gh_io.IGH, list) -> dict
    """Sorts all the FloorSegment Objects by 'Neighbor-Group' (if touching)

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _floor_segment_list (list[FloorSegments])

    Returns:
    --------
        * (dict): ie - {10947: set(FloorSegment_1, FloorSegment_2, ...), 10948: set(...), ... }
    """

    neighbor_groups = find_neighbors(IGH, _floor_segment_list)

    # -- Sort by Neighbor Group results
    floors_sorted_by_neighbor = defaultdict(list)
    for floor in _floor_segment_list:
        for _k, group_list_ids in neighbor_groups.items():
            if id(floor) in group_list_ids:
                floors_sorted_by_neighbor[_k].append(floor)

    return floors_sorted_by_neighbor


def create_Floors_from_FloorSegments(IGH, _room_dicts):
    # type: (gh_io, dict) -> dict
    """Creates new Floor Objects for the input FloorSegments. Sorts and groups
    new Floors by name / number and if the FloorSegments are 'touching'

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _room_dicts (dict): The Room dict to operate on

    Returns:
    --------
        * (dict): The room dicts, with the Floor Objects added to the 'Floor' key
    """

    for v in _room_dicts.values():
        v["Floors"] = {}

        for space_id, space_floor_segments_list in v["FloorSegments"].items():
            v["Floors"][space_id] = []
            results = sort_FloorSegments_by_neighbor(IGH, space_floor_segments_list)

            for floor_segment_group in results.values():

                new_floor = PHX.spaces.Floor()
                for floor_segment in floor_segment_group:
                    new_floor.add_new_floor_segment(floor_segment)

                v["Floors"][space_id].append(new_floor)

        del v["FloorSegments"]

    return _room_dicts
