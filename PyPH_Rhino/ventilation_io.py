# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Rhino/Grasshopper functions for buiding PHX Ventilation Systems, Ducts."""

import PHX.hvac_system
import PHX.hvac_components
import PyPH_Rhino.gh_io


class DuctInputError(Exception):
    def __init__(self, _in):
        self.message = 'Error: Cannot use input value: "{}" {} as the length ' "for Ventilation Duct?".format(
            _in, type(_in)
        )
        super(DuctInputError, self).__init__(self.message)


def handle_duct_input(IGH, _inputs, _input_node_name):
    # type: (PyPH_Rhino.gh_io.IGH, list, str) -> PHX.hvac_components.HVAC_Duct
    """Handle user-input of Ventilation ducts at the Ventilation-System level.

    Input could be:
        * Duct Object
        * A Duct Segment (?)
        * Text / float
        * Rhino Geom with attibutes
        * Rhono Geom without Attributes
        * Grasshopper Geom

    Arguments:
    ----------
        * IGH (PyPH_Rhino.gh_io): Grasshopper Interface
        * _inputs (list[Any]): The user input objects
        * _input_node_name (str): the name of the input node (for getting GUID values)

    Returns:
    --------
        * (PHX.hvac_components.HVAC_Duct): The new Ventilation Duct Object.
    """

    try:
        # -- If its RH/GH-Geom, Str, Float - handle all that
        clean_inputs = PyPH_Rhino.gh_io.handle_inputs(IGH, _inputs, _input_node_name)
        new_duct = PHX.hvac_components.HVAC_Duct()

        for _in in clean_inputs:
            # -- Build new Duct Segments
            new_duct_seg = PHX.hvac_components.HVAC_Duct_Segment()

            # -- Basic Duct Segment Params
            new_duct_seg.diameter = _in.get("ductDiameter", 0.0)
            new_duct_seg.width = _in.get("ductWidth", 0.0)
            new_duct_seg.height = _in.get("ductHeight")
            new_duct_seg.insulation_thickness = _in.get("insulThickness", 0.0)
            new_duct_seg.insulation_conductivity = _in.get("insulConductivity", 0.0)

            # -- Sort out the Duct Segment Length
            try:
                new_duct_seg.length = float(_in.get("Geometry"))
            except:
                try:
                    new_duct_seg.length = sum(float(geom) for geom in _in.get("Geometry"))
                except:
                    try:
                        new_duct_seg.length = sum(geo.length for geo in _in.get("Geometry"))
                    except AttributeError:
                        raise DuctInputError(_in.get("Geometry"))

            new_duct.segments.append(new_duct_seg)

        return new_duct

    except PyPH_Rhino.gh_io.LBTGeometryConversionError:
        # -- If input is not Geom or number, or string, could be HVAC Duct Objects
        new_ducts = []
        for _in in _inputs:
            if hasattr(_in, "segments"):
                # -- Is an Ventilation Duct already, so use that
                new_ducts.append(_in)
            else:
                raise DuctInputError(_in)

        new_duct = sum(new_ducts, start=PHX.hvac_components.HVAC_Duct())

        return new_duct
