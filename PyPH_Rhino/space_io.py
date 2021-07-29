# -*- coding: utf-8 -*-

"""Module documentation goes here
"""

def handle_input_geometry(IGH, _input, _input_name ): #-> list[dict]
    """Organize and standardize user inputs to the GH Component

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _input (list): The input node item(s) from the GH Component
        * _input_name (str): The name of the input node for the _floor_surfaces
    
    Returns:
    --------
        * list[dict]: Each dict is a single user-input entity with all of its 
            attributes from the Rhino UserText, and the input geometry converted 
            into ladybug geometry
    """

    if not isinstance(_input, list): _input = [ _input ]

    #-- Get the Input Object Attribute UserText values (if any)
    input_index_number = IGH.gh_compo_find_input_index_by_name(_input_name)
    input_guids = IGH.gh_compo_get_input_guids(input_index_number)
    inputs = IGH.get_rh_obj_UserText_dict(input_guids)
    
    #-- Add the Input Geometry to the output dictionary
    input_geometry = IGH.convert_to_LBT_geom( _input )
    for d,g in zip(inputs, input_geometry):
       d.update( {'Geometry':g} )

    return inputs
