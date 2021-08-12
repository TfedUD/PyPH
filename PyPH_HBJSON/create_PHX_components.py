# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to create 'Components' (surfaces / windows) from HB-JSON"""

import honeybee.face
import honeybee.aperture
import PHX.geometry
import PHX.bldg_segment
import PHX.component

# --- Opaque Components
# ------------------------------------------------------------------------------
def create_vertices_from_face(
    _hb_face: honeybee.face.Face,
) -> list[PHX.geometry.Vertex]:
    """Creates new Verts for each of the Vertices that make up a single Honeybee Face

    Arguments:
    ----------
        * _hb_face (honeybee.face.Face): The Honeybee Face to use as the source

    Returns:
    -------_
        * (list[PHX.geometry.Vertex]): A list of the new WP-Vertex objects, one for each HB-Vertex found
            on the input Honeybee Face
    """

    verts = []
    for vert in _hb_face.vertices:
        new_vert = PHX.geometry.Vertex()
        new_vert.x = vert.x
        new_vert.y = vert.y
        new_vert.z = vert.z

        verts.append(new_vert)

    return verts


def create_poly_from_HB_face(_hb_face: honeybee.face.Face) -> PHX.geometry.Polygon:
    """Creates a new Poly from a single Honeybee Face

    Arguments:
    ----------
        * _hb_face (honeybee.face.Face): The Honeybee face to use as the source for the new Poly

    Returns:
    --------
        * (PHX.geometry.Polygon): A new Poly object, based on the input Honeybee Face
    """

    # --- Create the new Poly bits and pieces from the HB Face
    if not _hb_face:
        return None

    poly = PHX.geometry.Polygon()
    poly.vertices = create_vertices_from_face(_hb_face)
    poly.nVec = _hb_face.normal

    return poly


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
    compo.n = _hb_face.display_name

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
        * _zones (list[PHX.bldg_segment.Zone]): A list of all the Zones in the bldg_segment.Building. This is
            needed in order to properly solve 'interior' faces with 'Surface' adjacency.

    Returns:
    --------
        * (PHX.component.Component.Component): The Component with the modified Exterior-Exposure value
    """

    # Translate Honeybee Exposure Type (str) into WUFI Exposure values (int)
    exterior_exposure_types = {
        "Outdoors": -1,
        "Ground": -2,
    }

    if _hb_face.boundary_condition.name == "Surface":
        # -- Apply defaults in case can't find the matching surface
        # -- This happens with inter-zone surfaces that are exposed to another
        # -- 'Case' (bldg_segment)

        ec_value = -3  # Adiabatic
        ec_attr = None

        # -- Try and set a real exposure by finding the opposing surface
        # -- Not Working yet......
        # for zone in _zones:
        #     if zone.identifier == _hb_face.boundary_condition.boundary_condition_objects[-1]:
        #         ec_value = zone.id
        #         ec_attr = zone.wp_display_name
    else:
        ec_value = exterior_exposure_types.get(_hb_face.boundary_condition.name, -1)
        ec_attr = None

    _compo.idEC = ec_value
    _compo.nmEC = ec_attr

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
    compo_color_by_bc = compo_color_by_srfc_type.get(
        _hb_face.boundary_condition.name, None
    )
    if compo_color_by_bc:
        _compo.id_color_int = compo_color_by_bc.get("int")
        _compo.id_color_ext = compo_color_by_bc.get("ext")

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
    _compo.idAssC = assembly.id

    return _compo


# --- Window Components
# -------------------------------------------------------------------------------
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
    window_compo.n = _hb_Aperture.display_name
    window_compo.type = 2  # Transparent
    window_compo.id_color_int = 4
    window_compo.id_color_ext = 4

    # -- Set Exposures / Host Zone
    window_compo.set_host_zone_name(_zone)
    window_compo.idEC = -1

    # -- Pack window Polygons onto the new Component
    window_compo.add_polygons(create_poly_from_HB_face(_hb_Aperture.geometry))

    return window_compo
