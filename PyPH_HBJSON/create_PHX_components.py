# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to create 'Components' (surfaces / windows) from HB-JSON"""

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D
import honeybee.face
import honeybee.shade
import honeybee.aperture
import PHX.geometry
import PHX.bldg_segment
import PHX.component

# --- Geometry Converters
# ------------------------------------------------------------------------------
def convert_LBT_Point3d_to_PHX_Vertices(_hb_verts: list[Point3D]) -> list[PHX.geometry.Vertex]:
    """Creates new PHX-Vertex for each of the Vertices that make up a single Honeybee Face

    Arguments:
    ----------
        * list[Point3D]: The list of Ladybug Point3D objects to convert to PHX Vertex objects

    Returns:
    -------_
        * (list[PHX.geometry.Vertex]): A list of the new WP-Vertex objects, one for each HB-Vertex found
            on the input Honeybee Face
    """

    verts = []
    for lbt_p3d in _hb_verts:
        new_vert = PHX.geometry.Vertex()
        new_vert.x = lbt_p3d.x
        new_vert.y = lbt_p3d.y
        new_vert.z = lbt_p3d.z

        verts.append(new_vert)

    return verts


def convert_LBT_Face3D_toPHX_Poly(_lbt_face: Face3D) -> PHX.geometry.Polygon:
    """Returns a new PHX-Polygon, based on a single LBT Face3D

    Arguments:
    ---------
        * _lbt_face (Face3D): The input Ladybug Face3D to use as the source for
            the new PHX-Polygon.

    Returns:
    --------
        * (PHX.geometry.Polygon)
    """
    if not _lbt_face:
        return None

    phx_Poly = PHX.geometry.Polygon()
    phx_Poly.vertices = convert_LBT_Point3d_to_PHX_Vertices(_lbt_face.vertices)
    phx_Poly.nVec = _lbt_face.normal  # convert?

    return phx_Poly


def create_poly_from_HB_face(_hb_face: honeybee.face.Face) -> PHX.geometry.Polygon:
    """Creates a new Poly from a single Honeybee Face

    Arguments:
    ----------
        * _hb_face (honeybee.face.Face): The Honeybee face to use as the source for the new Poly

    Returns:
    --------
        * (PHX.geometry.Polygon): A new Poly object, based on the input Honeybee Face
    """

    if not _hb_face:
        return None

    poly = PHX.geometry.Polygon()
    poly.vertices = convert_LBT_Point3d_to_PHX_Vertices(_hb_face.vertices)
    poly.nVec = _hb_face.normal  # convert?

    return poly


# --- Opaque Components
# ------------------------------------------------------------------------------
def create_new_opaque_component_from_hb_face(
    _hb_face: honeybee.face.Face,
) -> PHX.component.Component:
    """Creates a new Component based on an input HB-Face

    Arguments:
    ----------
        * _hb_face (honeybee.face.Face): The Honeybee Face(s) to use as the source for the new Component's Poly(s)

    Returns:
    --------
        * (PHX.component.Component): The new Component with attributes based on the input HB Face(s)
    """

    compo = PHX.component.Component()
    compo.name = _hb_face.display_name

    # -- Pack any polygons input onto the new Component
    if not isinstance(_hb_face, list):
        _hb_faces = [_hb_face]
    compo.polygons = [create_poly_from_HB_face(face) for face in _hb_faces]

    return compo


def set_compo_exterior_exposure_from_hb_face(
    _compo: PHX.component.Component,
    _hb_face: honeybee.face.Face,
    _zones: list[PHX.bldg_segment.Zone],
) -> PHX.component.Component:
    """Sets a Component's Exterior-Exposure Value based on a Honeyebee Face

    Arguments:
    ----------
        * _compo (PHX.component.Component): The Component to set the Exterior-Exposure values for
        * _hb_face (honeybee.face.Face): The Honeybee Face to base the Component's Exterior-Exposure type on
        * _zones (list[PHX.bldg_segment.Zone]): A list of all the Zones in the bldg_segment.zones. This is
            needed in order to properly solve 'interior' faces with 'Surface' adjacency.

    Returns:
    --------
        * (PHX.component.Component.Component): The Component with the modified Exterior-Exposure value
    """

    # Translate Honeybee Exposure Type (str) into WUFI Exposure values (int)
    exterior_exposure_types = {
        "Outdoors": -1,
        "Ground": -2,
        "Adiabatic": -3,
        "Surface": -3,
    }

    if "SURFACE" in str(_hb_face.boundary_condition.name).upper():
        # -- Apply defaults in case can't find the matching surface
        # -- This happens with inter-zone surfaces that are exposed to another
        ec_value = -3  # Adiabatic
        ec_attr = None
    elif "ADIABATIC" in str(_hb_face.boundary_condition.name).upper():
        ec_value = -3  # Adiabatic
        ec_attr = None
    else:
        ec_value = exterior_exposure_types.get(_hb_face.boundary_condition.name, -1)
        ec_attr = None

    _compo.ext_exposure_zone_id = ec_value
    _compo.ext_exposure_zone_name = ec_attr

    return _compo


def set_compo_colors_by_hb_face(
    _compo: PHX.component.Component, _hb_face: honeybee.face.Face
) -> PHX.component.Component:
    """Sets the Interior and Exterior Component Colors based on a Honeybee Face's Type (Wall | RoofCeiling | Floor)

    Arguments:
    ----------
        * _compo (PHX.component.Component): The Component to set the colors for
        * _hb_face (honeybee.face.Face): The Honeybee Face to base the color settings on

    Returns:
    --------
        * (PHX.component.Component): The Component with modified colors applied
    """

    colors = {
        "Wall": {
            "Outdoors": {"ext": 2, "int": 1},
            "Surface": {"ext": 3, "int": 3},
            "Ground": {"ext": 12, "int": 14},
            "Adiabatic": {"ext": 3, "int": 3},
        },
        "RoofCeiling": {
            "Outdoors": {"ext": 10, "int": 11},
            "Surface": {"ext": 6, "int": 6},
            "Ground": {"ext": 12, "int": 13},
            "Adiabatic": {"ext": 6, "int": 6},
        },
        "Floor": {
            "Outdoors": {"ext": 5, "int": 5},
            "Surface": {"ext": 5, "int": 5},
            "Ground": {"ext": 12, "int": 13},
            "Adiabatic": {"ext": 5, "int": 5},
        },
        "AirBoundary": {
            "Outdoors": {"ext": 3, "int": 3},
            "Surface": {"ext": 3, "int": 3},
            "Ground": {"ext": 3, "int": 3},
            "Adiabatic": {"ext": 3, "int": 3},
        },
    }

    compo_color_by_srfc_type = colors.get(_hb_face.type.name, {})
    compo_color_by_bc = compo_color_by_srfc_type.get(_hb_face.boundary_condition.name, None)
    if compo_color_by_bc:
        _compo.int_color_id = compo_color_by_bc.get("int")
        _compo.ext_color_id = compo_color_by_bc.get("ext")

    return _compo


def set_compo_assembly_from_hb_face(
    _compo: PHX.component.Component, _hb_face: honeybee.face.Face, _assembly_collection
) -> PHX.component.Component:
    """Sets a Component's 'IdentNrAssembly' based on the Assembly name from a Honeybee Face

    Arguments:
    ----------
        * _compo (PHX.component.Component): The Component to set the Assembly of
        * _hb_face (honeybee.face.Face): The Honeybee Face. Will use the Face's Assembly Name as the key
        * _assembly_collection (AssemblyCollection): The Project's Assembly Collection with all the Assembly Information

    Returns:
    --------
        * (Component): The Component with the 'IdentNrAssembly' set based on the Honeybee Face Assembly
    """

    hb_construction_identifier = _hb_face.properties.energy.construction.identifier
    assembly = _assembly_collection.get_assembly_by_name(hb_construction_identifier)
    _compo.assembly_id_num = assembly.id

    return _compo


# --- Window Components
# ------------------------------------------------------------------------------
def create_new_window_component_from_hb_aperture(
    _hb_Aperture: honeybee.aperture.Aperture, _zone: PHX.bldg_segment.Zone
) -> PHX.component.Component:
    """Creates a new Window Component from a Honeybee 'Aperture'

    Arguments:
    ----------
        * _hb_Aperture (honeybee.aperture.Aperture): The Honeybee Aperture to use as the source for the new Component's Poly.
        * _zone (PHX.bldg_segment.Zone): The Host Zone which the new Winow Component is associate with.

    Returns:
    --------
        * (PHX.component.Component): The new Window Component with attributes based on the input HB-Aperture.
    """

    window_compo = PHX.component.Component()

    # -- Basic Component Attributes
    window_compo.name = _hb_Aperture.display_name
    window_compo.type = 2  # Transparent
    window_compo.int_color_id = 4
    window_compo.ext_color_id = 4

    # -- Set Exposures / Host Zone
    window_compo.set_host_zone_name(_zone)
    window_compo.ext_exposure_zone_id = -1

    # -- Pack window Polygons onto the new Component
    window_compo.add_polygons(create_poly_from_HB_face(_hb_Aperture.geometry))

    return window_compo


# --- Shade Components
# ------------------------------------------------------------------------------
def set_exposures_for_shade(_shade_compo: PHX.component.Component) -> PHX.component.Component:
    """Sets a Component's indoor and outdoor exposure to 'Outer-air', which means: shading

    Arguments:
    ---------
        * _shade_compo (PHX.component.Component): The shade component to edit.
    Returns:
    --------
        * (PHX.component.Component) The Component with the values changed.
    """

    _shade_compo.ext_exposure_zone_id = -1
    _shade_compo.ext_exposure_zone_name = "Outer air"

    _shade_compo.int_exposure_zone_id = -1
    _shade_compo.int_exposure_zone_name = "Outer air"

    return _shade_compo


def create_new_shade_component(_HB_shade: honeybee.shade.Shade):
    """Creates a new 'Shade' PHX-Component Object, based on a honeybee.shade.Shade

    Arguments:
    ----------
        * _HB_shade (honeybee.shade.Shade): The Honeybee Shade to use as the source.

    Returns:
    --------
        * PHX.component.Component): The new PHX Component with 'shade' properties.
    """

    shade_compo = PHX.component.Component()
    shade_compo.name = _HB_shade.display_name

    # -- Pack the shade Polygon onto the new Component
    shade_compo.polygons = [convert_LBT_Face3D_toPHX_Poly(_HB_shade.geometry)]
    shade_compo = set_exposures_for_shade(shade_compo)

    return shade_compo
