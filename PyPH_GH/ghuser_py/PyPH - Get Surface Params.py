#
# PyPH: A Plugin for aadding Passive-House data to LadybugTools Models
# 
# This component is part of the PH-Tools toolkit <https://github.com/PH-Tools>.
# 
# Copyright (c) 2021, PH-Tools and bldgtyp, llc <phtools@bldgtyp.com> 
# PyPH is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# PyPH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# For a copy of the GNU General Public License
# see <https://github.com/PH-Tools/PyPH/blob/main/LICENSE>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
#
"""
Use this component BEFORE a Honeybee 'Face' component. This will pull data from  
the Rhino scene (names, constructions, etc) where relevant. Simply connect the  
outputs from this compone to the inputs on the 'Face' for this to run.
-
EM August 20, 2021
    Args:
        _surfaces: (list) Rhino Surface geometry.
    Returns:
        geo_: Connect to the '_geo' Input on a Honeybee 'Face' component.
        name_: Names found on the Rhino geometry (Rhino ObjectName). Connect 
            to the '_name' Input on a Honeybee 'Face' component.
        type_: Surface type (wall, roof, floor) Connect to the '_type' 
            Input on a Honeybee 'Face' component.
        bc_: Connect to the '_bc' Input on a Honeybee 'Face' component. If 
            blank or any Null values pased, will use HB defaults as usual.
        ep_const_: Connect to the 'ep_constr_' Input on a Honeybee 'Face' 
            component. If blank or any Null values pased, will use HB defaults as usual.
        rad_mod_: <Not implemented yet>
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

from System import Object
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree

import PyPH_Rhino
import PyPH_Rhino.surfaces
import PyPH_Rhino.gh_io


# --- 
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Get Surface Params"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='AUG 20, 2021')

if DEV:
    reload( PyPH_Rhino)
    reload(PyPH_Rhino.surfaces)
    reload(PyPH_Rhino.gh_io)

#--- Handle all the inputs, get list of input object dicts
IGH = PyPH_Rhino.gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

geo_ = DataTree[Object]()
name_ = DataTree[Object]()
type_ = DataTree[Object]()
bc_ = DataTree[Object]()
ep_const_ = DataTree[Object]()
rad_mod_ = DataTree[Object]()

# --
for i, b in enumerate(_surfaces.Branches):
    b = list(b)
    input_objects = PyPH_Rhino.gh_io.handle_inputs(IGH, b, '_surfaces', i)
    
    #--- Clean and organize the inputs
    input_objects = PyPH_Rhino.surfaces.set_orientation(IGH, input_objects)
    input_objects = PyPH_Rhino.surfaces.set_names(input_objects)
    input_objects = PyPH_Rhino.surfaces.set_type(input_objects)
    input_objects = PyPH_Rhino.surfaces.set_EPConstruction(input_objects)
    input_objects = PyPH_Rhino.surfaces.convert_geom_to_rh(IGH, input_objects)
    
    #-------------------------------------------------------------------------------
    # Package up the Outputs
    for input_object in input_objects:
        geo_.Add( input_object.get('Geometry'), GH_Path(i) )
        name_.Add( input_object.get('Object Name'), GH_Path(i) )
        type_.Add( input_object.get('srfType'), GH_Path(i))
        bc_.Add( input_object.get('EPBC'), GH_Path(i))
        ep_const_.Add( input_object.get('EPConstruction'), GH_Path(i) )
        rad_mod_.Add( input_object.get('RadMod'), GH_Path(i))