# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""IO handler for Rhino user-input Floor-Surface geometry objects"""

import gh_io


def handle_input_geometry(IGH, _input_objects, _input_name):
    # type: (gh_io.IGH, list, str) -> list[dict]
    """Organize and standardize user inputs to the GH Component

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _input_objects (list): The input node item(s) from the GH Component
        * _input_name (str): The name of the input node for the _floor_surfaces

    Returns:
    --------
        * list[dict]: Each dict is a single user-input entity with all of its
            attributes from the Rhino UserText, and the input geometry converted
            into ladybug geometry
    """

    if not isinstance(_input_objects, list):
        _input_objects = [_input_objects]

    # -- Get the Input Object Attribute UserText values (if any)
    input_index_number = IGH.gh_compo_find_input_index_by_name(_input_name)
    input_guids = IGH.gh_compo_get_input_guids(input_index_number)
    inputs = IGH.get_rh_obj_UserText_dict(input_guids)

    # -- Add the Input Geometry to the output dictionary
    input_geometry = IGH.convert_to_LBT_geom(_input_objects)
    for d, g in zip(inputs, input_geometry):
        d.update({"Geometry": g})

    return inputs
