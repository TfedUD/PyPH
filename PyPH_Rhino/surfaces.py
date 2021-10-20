# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Rhino/Grasshopper functions for building PHX Envelope Surfaces"""

import random
import math
import ladybug_geometry.geometry3d
import PyPH_Rhino.gh_io

import honeybee.boundarycondition
import honeybee.face


def set_orientation(IGH, _input_objects):
    # type: (PyPH_Rhino.gh_io.IGH, list[dict]) -> list[dict]
    """Sets the input object's 'Type' (floor, wall, roof) based on the surface normal direction

    Arguments:
    ----------
        * IGH (PyPH_Rhino.gh_io.IGH):
        * _input_obects (list[dict]): The input objects to use.

    Returns:
    --------
        list[dict]: The input objects with their 'Type' changed as approrpriate
    """

    # Code here adapted from Honeybee Legacy 'decomposeZone' method
    # Checks the surface normal and depending on the direction,
    # assigns it as a 'wall', 'floor' or 'roof'

    MAX_ROOF_ANG = 30

    for obj in _input_objects:
        # -- Find the input object's average surface normal
        normal = ladybug_geometry.geometry3d.Vector3D(0, 0, 0)
        face_list = obj.get("Geometry")
        for face in face_list:
            normal += face.normal

        # -- Find the surface type based on the normal
        angle2Z = math.degrees(normal.angle(ladybug_geometry.geometry3d.Vector3D(0, 0, 1)))
        existing_exposure = str(obj.get("EPBC")).upper()

        if angle2Z < MAX_ROOF_ANG or angle2Z > 360 - MAX_ROOF_ANG:
            # -- Must be a roof
            obj["srfType"] = "RoofCeiling"
            if ("ADIABATIC" not in existing_exposure) and ("OUTDOORS" not in existing_exposure):
                obj["EPBC"] = "Outdoors"
        elif 160 < angle2Z < 200:
            # -- Must be a floor
            obj["srfType"] = "Floor"
            if ("ADIABATIC" not in existing_exposure) and ("OUTDOORS" not in existing_exposure):
                obj["EPBC"] = "Ground"
        else:
            # -- Must be a Wall
            obj["srfType"] = "Wall"
            if ("ADIABATIC" not in existing_exposure) and ("OUTDOORS" not in existing_exposure):
                obj["EPBC"] = "Outdoors"

    return _input_objects


def set_EPConstruction(_input_objects):

    return _input_objects


def set_type(_input_objects, _lbt_version="lbt1"):
    # type: (list[dict], str) -> list[dict]
    """Clean the input 'Type' (wall, floor, etc). Converts names to LBT version 1 format

    Arguments:
    ----------
        * _input_objects (list[dict]): The input objects
        * _lbt_version (str): default='lbt1'

    Returns:
    --------
        * list[dict]: The input objects, with their 'Type' modified
    """

    srfc_type_schema = {
        "Wall": {"legacy": 0, "lbt1": "Wall"},
        "WALL": {"legacy": 0, "lbt1": "Wall"},
        "UndergroundWall": {"legacy": 0.5, "lbt1": "Wall"},
        "ROOF": {"legacy": 1, "lbt1": "RoofCeiling"},
        "Roof": {"legacy": 1, "lbt1": "RoofCeiling"},
        "UndergroundCeiling": {"legacy": 1.5, "lbt1": "Wall"},
        "FLOOR": {"legacy": 2, "lbt1": "Floor"},
        "Floor": {"legacy": 2, "lbt1": "Floor"},
        "UndergroundSlab": {"legacy": 2.25, "lbt1": "Floor"},
        "SlabOnGrade": {"legacy": 2.5, "lbt1": "Floor"},
        "ExposedFloor": {"legacy": 2.75, "lbt1": "Floor"},
        "RoofCeiling": {"legacy": 3, "lbt1": "RoofCeiling"},
        "CEILING": {"legacy": 3, "lbt1": "RoofCeiling"},
        "AIRWALL": {"legacy": 4, "lbt1": "AirBoundary"},
        "WINDOW": {"legacy": 5, "lbt1": "Wall"},
        "SHADING": {"legacy": 6, "lbt1": "Wall"},
    }

    for obj in _input_objects:
        input_type = str(obj.get("srfType", "WALL"))
        obj["srfType"] = srfc_type_schema.get(input_type, "Wall").get(_lbt_version)

    return _input_objects


def _get_default_name(_d):
    # type: (dict) -> str
    """Returns a default name, if no user-defined name is input."""

    nm = _d.get("Object Name")

    if not nm:
        return "No_Name_{}".format(random.randint(100000, 999999))
    else:
        return nm


def _get_name_with_exposure_flag(_d):
    # type: (dict) -> str
    """
    So that the EP Results can be properly sorted at the very end,
    add an 'EXT_' or 'INT_' 'flag' to the object.

    ie: if the BC=='Adiabatic', 'My_Name' --> 'INT_My_Name'
        if the BC!='Adiabatic', 'My_Name' --> 'EXT_MY_Name'

    Arguments:
    ----------
        * _d (dict): The Object dictionary to work with

    Returns:
    --------
        * (str): The new name

    """

    nm = str(_d.get("Object Name"))
    bc = str(_d.get("EPBC"))

    if "ADIABATIC" in bc.upper():
        return "INT_{}".format(nm)
    else:
        return "EXT_{}".format(nm)


def set_names(_input_objects):
    # type: (list[dict]) -> list[dict]
    """Cleans and sets the names of input objects"""

    for input_object in _input_objects:
        input_object["Object Name"] = _get_default_name(input_object)
        input_object["Object Name"] = _get_name_with_exposure_flag(input_object)

    return _input_objects


def convert_geom_to_rh(IGH, _input_objects):
    # type: (PyPH_Rhino.gh_io.IGH, list[dict]) -> list[dict]
    """Converts the input Object Geometry over to Rhino Geom for the Honeybee Components

    Arguments:
    ----------
        * IGH (PyPH_Rhino.gh_io.IGH):
        * _input_obects (list[dict]): The input objects to use.

    Returns:
    --------
        list[dict]: The input objects with their geometry converted to Rhino Objects
    """

    new_objs = []

    for obj in _input_objects:
        g = obj.get("Geometry")
        rh_geom = IGH.convert_to_rhino_geom(g)

        for each in rh_geom:
            new_obj = obj
            new_obj["Geometry"] = each
            new_objs.append(new_obj)

    return new_objs


def set_HB_face_BC_to_adiabatic_if_match_not_found(_face, _set_of_potential_matches):
    # type: (honeybee.face.Face, set[str]) -> None
    """Compares a HB Surface to a set of potential matches, and if none are found, sets its BC as Adiabatic

    This is used when splitting a model into multiple Building Segments. For any Seg<->Seg
    surfaces, reset their BC to Adiabatic rather than 'Surface'

    Arguments:
    ----------
        * _face (honeybee.face.Face): The Honeybee Face to modify the BC on.
        * _set_of_potential_matches (set[str]): A list of potential matching / adjacent surface identifiers.

    Returns:
    --------
        * None
    """

    if _face.boundary_condition.boundary_condition_object not in _set_of_potential_matches:
        _face.boundary_condition = honeybee.boundarycondition.boundary_conditions.by_name("Adiabatic")

    return None
