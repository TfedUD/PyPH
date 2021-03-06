# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Grasshopper Interface Class. Used to pass Rhino, GH side dependancies to all other classes.

This is done so that other classes can be tested by mocking out this Interface. If I 
could figure out how to get Rhino dependancies to be recognized by testing framework, 
probably would not need something like this? I suppose it does help reduce coupling?
"""

from contextlib import contextmanager
from itertools import izip_longest
from copy import deepcopy

import honeybee.face
from ladybug_rhino.togeometry import (
    to_face3d,
    to_linesegment3d,
    to_mesh3d,
    to_point3d,
    to_polyline3d,
)
from ladybug_rhino.fromgeometry import (
    from_face3d,
    from_linesegment3d,
    from_mesh3d,
    from_point3d,
    from_polyline3d,
)


class SelectionInputError(Exception):
    def __init__(self, _in):
        self.message = 'Input Error: Cannot use input "{}" [{}].\n' "Please check the allowable input options.".format(
            _in, type(_in)
        )

        super(SelectionInputError, self).__init__(self.message)


class LBTGeometryConversionError(Exception):
    def __init__(self, _in):
        self.message = 'Input Error: Cannot convert "{}" to LBT Geometry.'.format(type(_in))

        super(LBTGeometryConversionError, self).__init__(self.message)


class IGH:
    """PyPH Interface for basic Grasshopper (and Rhino) dependancies that can be
        used by other classes which accept this Interface object.

    Arguments:
    ----------
        * _ghdoc: (ghdoc)
        * _ghenv: (ghenv)
        * _sc: (scriptcontext)
        * _rh: (Rhino)
        * _rs (rhinoscriptsyntax)
    """

    def __init__(self, _ghdoc, _ghenv, _sc, _rh, _rs, _ghc, _gh):
        self.ghdoc = _ghdoc
        self.ghenv = _ghenv
        self.scriptcontext = _sc
        self.Rhino = _rh
        self.rhinoscriptsyntax = _rs
        self.grasshopper_components = _ghc
        self.Grasshopper = _gh

    def gh_compo_find_input_index_by_name(self, _input_name):
        # type: (str) -> int
        """
        Compares an input name against the list of GH_Component Inputs. Returns the
        index of any match or None if not found

        Arguments:
        ----------
            * _input_name (str): The name to search for

        Returns:
        --------
            * (int): The index of the matching item
        """

        for i, each in enumerate(list(self.ghenv.Component.Params.Input)):
            names = [str(each.Name).upper(), str(each.NickName).upper()]
            if _input_name.upper() in names:
                return i

        raise Exception('Error: The input node "{}" cannot be founnd?'.format(_input_name))

    def gh_compo_get_input_for_node_number(self, _node_number):
        return self.ghenv.Component.Params.Input[_node_number].VolatileData

    def gh_compo_get_input_guids(self, _input_index_number, _branch_num=0):
        # type: (int, int) -> list[System.Guid]
        """
        Returns a list of all the GUIDs of the objects being passed to the
        component's specified input node.

        Arguments:
        ----------
            * _input_index_number (int): The index number of the input node to
                look at.

        Returns:
        --------
            * list[System.Guid]: The GUIDs of the objects being input into the specified
                component input node.
        """

        guids = []
        try:
            for _ in self.ghenv.Component.Params.Input[_input_index_number].VolatileData[_branch_num]:
                try:
                    guids.append(_.ReferenceID)
                except AttributeError:
                    # If input doesn't have a ReferenceID, its probably a Panel text or number input
                    guids.append(None)
        except ValueError:
            nm = self.ghenv.Component.Params.Input[_input_index_number].NickName
            print('No input values found for "{}".'.format(nm))

        return guids

    @contextmanager
    def context_rh_doc(self):
        """
        Context Manager used to switch Grasshopper's scriptcontext.doc
        to Rhino.RhinoDoc.ActiveDoc temporaily. This is needed when trying
        to access information such as UserText for Rhino objects

        Use:
        ----
        >>> with context_rh_doc():\n
        >>>    run_some_command( gh_component_input )
        """

        try:
            self.scriptcontext.doc = self.Rhino.RhinoDoc.ActiveDoc
            yield
        except Exception as e:
            self.scriptcontext.doc = self.ghdoc
            print("Exception:", e.message)
            raise Exception
        finally:
            self.scriptcontext.doc = self.ghdoc

    def get_rh_obj_UserText_dict(self, _rh_obj_guids):
        # type: (System.guid) -> list[dict]
        """
        Get any Rhino-side UserText attribute data for the Object/Elements.
        Note: this only works in Rhino v6.0+ I believe...

        Arguments:
        ----------
            _rh_obj_guids list(Rhino Guid): The Rhino Guid(s) of the Object/Elements.

        Returns:
        --------
            output_list list[dict]: A list of dictionaries, each with all the data found
                in the Rhino object's UserText library.
        """

        def is_grasshopper_geometry(_guid):
            """If its GH generated geom, will have this GUID always"""
            return str(_guid) == "00000000-0000-0000-0000-000000000000"

        if not _rh_obj_guids:
            return []
        if not isinstance(_rh_obj_guids, list):
            _rh_obj_guids = [_rh_obj_guids]

        output_list = []
        with self.context_rh_doc():
            for guid in _rh_obj_guids:
                if not guid or is_grasshopper_geometry(guid):
                    output_list.append({"Object Name": None})
                else:
                    # -- Go get the data from Rhino
                    rh_obj = self.Rhino.RhinoDoc.ActiveDoc.Objects.Find(guid)
                    object_rh_UserText_dict = {
                        k: self.rhinoscriptsyntax.GetUserText(rh_obj, k)
                        for k in self.rhinoscriptsyntax.GetUserText(rh_obj)
                    }

                    # -- Fix the name
                    object_name = self.rhinoscriptsyntax.ObjectName(guid)
                    object_rh_UserText_dict["Object Name"] = object_name

                    output_list.append(object_rh_UserText_dict)

        return output_list

    def convert_to_LBT_geom(self, _inputs):
        # type: (list) -> list
        """Converts a list of RH- or GH-Geometry into a list of LBT-Geometry. If
            input is a string, boolean or number, will just return that without converting.
        Arguments:
        ----------
            * _inputs (list): The Rhino items / objects to try and convert
        Returns:
        --------
            * list: The input (RH/GH) geometry, converted to LBT-Geometry
        """

        if not isinstance(_inputs, list):
            _inputs = [_inputs]
        lbt_geometry = []
        for i, _ in enumerate(_inputs):
            if isinstance(_, list):
                for __ in _:
                    result = self.convert_to_LBT_geom(__)
                    lbt_geometry.append(result)
            elif isinstance(_, (str, int, float)):
                try:
                    lbt_geometry.append(float(str(_)))
                except ValueError:
                    lbt_geometry.append(str(_))
            elif isinstance(_, bool):
                lbt_geometry.append(_)
            elif isinstance(_, self.Rhino.Geometry.Brep):
                lbt_geometry.append(to_face3d(_))
            elif isinstance(_, self.Rhino.Geometry.PolylineCurve):
                lbt_geometry.append(to_polyline3d(_))
            elif isinstance(_, self.Rhino.Geometry.LineCurve):
                lbt_geometry.append(to_linesegment3d(_))
            elif isinstance(_, self.Rhino.Geometry.Line):
                lbt_geometry.append(to_linesegment3d(self.Rhino.Geometry.LineCurve(_)))
            elif isinstance(_, self.Rhino.Geometry.Mesh):
                lbt_geometry.append(to_mesh3d(_))
            elif isinstance(_, self.Rhino.Geometry.Point3d):
                lbt_geometry.append(to_point3d(_))
            else:
                raise LBTGeometryConversionError(_)

        return lbt_geometry

    def convert_to_rhino_geom(self, _inputs):
        # type: (list) -> list
        """Converts a list of LBT-Geometry into RH-Geometry.

        Arguments:
        ----------
            * _inputs (list): The LBT Geometry items / objects to try and convert

        Returns:
        --------
            * list: The input LBT geometry, converted to Rhino-Geometry
        """

        if not isinstance(_inputs, list):
            _inputs = [_inputs]

        rh_geom = []
        for _ in _inputs:
            if isinstance(_, list):
                for __ in _:
                    result = self.convert_to_rhino_geom(__)
                    rh_geom.append(result)
            elif isinstance(_, honeybee.face.Face):
                rh_geom.append(from_face3d(_.geometry))
            elif isinstance(_, honeybee.face.Face3D):
                rh_geom.append(from_face3d(_))
            else:
                raise Exception('Input Error: Cannot convert "{}" to Rhino Geometry.'.format(type(_)))

        return rh_geom

    def inset_LBT_face(self, _lbt_face, _inset_distance):
        # type: (honeybee.face.Face, float) -> list
        """Converts an LBT face to Rhino Geom and performs an 'inset' operation on it. Returns the newly inset Face3D

        Arguments:
        ----------
            * _lbt_face (honeybee.face.Face): The LBT Face to inset
            * _inset_distance (float): The distance to inset the surface

        Returns:
        --------
            * (honeybee.face.Face): A new LBT Face, inset by the specified amount
        """

        rh_floor_surface = self.convert_to_rhino_geom(_lbt_face)

        if _inset_distance < 0.001:
            return rh_floor_surface

        # -----------------------------------------------------------------------
        srfcPerim = self.grasshopper_components.JoinCurves(
            self.grasshopper_components.BrepEdges(rh_floor_surface)[0], preserve=False
        )

        # Get the inset Curve
        # -----------------------------------------------------------------------
        srfcCentroid = self.Rhino.Geometry.AreaMassProperties.Compute(rh_floor_surface).Centroid
        plane = self.grasshopper_components.XYPlane(srfcCentroid)
        plane = self.grasshopper_components.IsPlanar(rh_floor_surface, True).plane
        srfcPerim_Inset_Pos = self.grasshopper_components.OffsetCurve(srfcPerim, _inset_distance, plane, 1)
        srfcPerim_Inset_Neg = self.grasshopper_components.OffsetCurve(srfcPerim, _inset_distance * -1, plane, 1)

        # Choose the right Offset Curve. The one with the smaller area
        # Check IsPlanar first to avoid self.grasshopper_components.BoundarySurfaces error
        # -----------------------------------------------------------------------
        if srfcPerim_Inset_Pos.IsPlanar:
            srfcInset_Pos = self.grasshopper_components.BoundarySurfaces(srfcPerim_Inset_Pos)
        else:
            srfcInset_Pos = self.grasshopper_components.BoundarySurfaces(srfcPerim)  # Use the normal perim

        if srfcPerim_Inset_Neg.IsPlanar():
            srfcInset_Neg = self.grasshopper_components.BoundarySurfaces(srfcPerim_Inset_Neg)
        else:
            srfcInset_Neg = self.grasshopper_components.BoundarySurfaces(srfcPerim)  # Use the normal perim

        # -----------------------------------------------------------------------
        area_Pos = self.grasshopper_components.Area(srfcInset_Pos).area
        area_neg = self.grasshopper_components.Area(srfcInset_Neg).area

        if area_Pos < area_neg:
            return self.convert_to_LBT_geom(srfcInset_Pos)
        else:
            return self.convert_to_LBT_geom(srfcInset_Neg)

    def merge_Face3D(self, _face3Ds):
        # type: (honeybee.face.Face3D) -> list[ list[honeybee.face.Face3D] ]
        """Combine a set of Face3D surfaces together into 'merged' Face3Ds

        This *should* work on surfaces that are touching, AND ones that overlap. Using
        GH MergeFaces() only works on 'touching' surfaces, but not overlapping ones.
        Using 'RegionUnion' should work on both touching and overlapping srfcs.

        Arguments:
        ----------
            * _face3Ds (list[honeybee.face.Face3D]): The Face3Ds to try and merge

        Returns:
        --------
            * (list[list[honeybee.face.Face3D]]): The merged Face3Ds
        """

        # -- Pull out the Perimeter curves from each Face3D
        perims = []
        for face3D in _face3Ds:
            rh_brep = self.convert_to_rhino_geom(face3D)
            faces, edges, vertices = self.grasshopper_components.DeconstructBrep(rh_brep)
            perims.append(self.grasshopper_components.JoinCurves(edges, True))

        joined_curves = self.grasshopper_components.RegionUnion(perims)

        if not isinstance(joined_curves, list):
            joined_curves = [joined_curves]

        # -- Intersect and Merge the Perimeter Curves back togther, make new Face3Ds
        new_LBT_face3ds = []
        for crv in joined_curves:
            merged_breps = self.Rhino.Geometry.Brep.CreatePlanarBreps(crv, 0.01)

            for new_brep in merged_breps:
                new_LBT_Face = self.convert_to_LBT_geom(new_brep)
                new_LBT_face3ds.extend(new_LBT_Face)

        return new_LBT_face3ds

    def warning(self, _in):
        """Raise a runtime Warning message on the GH Component"""
        if not _in:
            return None
        else:
            level = self.Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning
            self.ghenv.Component.AddRuntimeMessage(level, _in)


def handle_inputs(IGH, _input_objects, _input_name, _branch_num=0):
    # type: (IGH, list, str, int) -> list[dict]
    """
    Generic Rhino / GH Geometry input handler

    Arguments:
    ----------
        * IGH (PyPH_Rhino.gh_io.IGH)
        * _input_objects (Any):
        * _input_name (str):

    Returns:
    --------
        (list[dict]): A list of the object dictionaries with all the information found.
    """

    if not isinstance(_input_objects, list):
        _input_objects = list(_input_objects)

    # -- Get the Input Object Attribute UserText values (if any)
    input_index_number = IGH.gh_compo_find_input_index_by_name(_input_name)
    input_guids = IGH.gh_compo_get_input_guids(input_index_number, _branch_num)
    inputs = IGH.get_rh_obj_UserText_dict(input_guids)

    # -- Add the Input Geometry to the output dictionary
    input_geometry_lists = IGH.convert_to_LBT_geom(_input_objects)

    output_list = []
    for input_dict, geometry_list in zip(inputs, input_geometry_lists):
        if not isinstance(geometry_list, list):
            geometry_list = [geometry_list]

        for geometry in geometry_list:
            item = deepcopy(input_dict)
            item.update({"Geometry": [geometry]})
            output_list.append(item)

    return output_list


def input_to_int(IGH, _input_value, _default=None):
    """For 'selection' type inputs, clean and convert input to int.

    ie: if the Grasshopper input allows:
        "1-A First Type"
        "2-A Second Type"

    will strip the string part and return just the integer value, or error.

    """

    if _input_value is None:
        return _default

    try:
        return int(_input_value)
    except ValueError as e:
        try:
            r = str(_input_value).split("-")
            return int(r[0])
        except ValueError as e2:
            raise SelectionInputError(_input_value)
