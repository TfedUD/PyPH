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
Collects and organizes data for a duct for a Ventilation System.
-
EM August 25, 2021
    Args:
        _duct_length: List<Float | Curve> Input either a number for the length of 
            the duct from the Ventilation Unit to the building enclusure, or geometry 
            representing the duct (curve / line)
        duct_width_: List<Float> Input the diameter (mm) of the duct. Default is 101mm (4")
        duct_height_: 
        duct_diameter_:
        insulation_thickness_: List<Float> Input the thickness (mm) of insulation on the
            duct. Default is 52mm (2")
        insulation_conductivity_: List<Float> Input the Lambda value (W/m-k) of the 
            insualtion. Default is 0.04 W/mk (Fiberglass)
    Returns:
        duct_: A Duct object for the Ventilation System. Connect to the 
            'hrvDuct_01_' or 'hrvDuct_02_' input on the 'Create Vent System' to 
            build a PHPP-Style Ventialtion System.
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

import PyPH_Rhino.ventilation_io
import PyPH_Rhino.gh_io

# --
import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.name = "PyPH - Ventilation Duct"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="AUG 25, 2021")

if DEV:
    reload(PyPH_Rhino.ventilation_io)
    reload(PyPH_Rhino.gh_io)


def clean(input_list, i):
    try:
        return input_list[i]
    except IndexError:
        try:
            return input_list[0]
        except IndexError:
            return None


# -- Interface Object
# -------------------------------------------------------------------------------
IGH = PyPH_Rhino.gh_io.IGH(ghdoc, ghenv, sc, rh, rs, ghc, gh)


# -- Get user inputs
# -------------------------------------------------------------------------------
duct_ = PyPH_Rhino.ventilation_io.handle_duct_input(IGH, _duct_length, "_duct_length")

for i, segment in enumerate(duct_.segments):
    segment.width = clean(duct_width_, i) or segment.width
    segment.height = clean(duct_height_, i) or segment.height
    segment.diameter = clean(duct_diameter_, i) or segment.diameter
    segment.insulation_thickness = clean(insulation_thickness_, i) or segment.insulation_thickness
    segment.insulation_conductivity = clean(insulation_conductivity_, i) or segment.insulation_conductivity
