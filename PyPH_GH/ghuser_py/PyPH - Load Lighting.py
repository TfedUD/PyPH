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
Modify a Honeybee 'HB Lighting' Program by adding Passive House style attributes.
-----
-
EM October 08, 2021
    Args:
        _name: (str) The name for the new Honeybee Lighting Program.
        _base: (Honeybee Lighting Program): The 'base' Honeybee lighting program that 
            the new Passive House style attributes should be added to.
        illumination_level_: (lux) The lux target at the illumination plane.
        illumination_height_: (m) The height of the target illumination plane
            above floor level.
    Returns:
        lighting_: The input Honeybee Lighting program, with new Passive House style 
            attributes added. This can be applied directly to a Honeybee Room, using 
            'HB Apply ProgramType' or used to create an HB Program.
"""

import PHX
import PHX.programs.loads
import PHX.programs.lighting
import PyPH_Rhino.gh_utils
import LBT_Utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Load Lighting"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_08_2021')

if DEV:
    reload(PHX.programs.loads)
    reload(PHX.programs.lighting)
    reload(PHX.programs.schedules)
    reload(PyPH_Rhino.gh_utils)
    reload(PHX.serialization.to_dict)
    reload(LBT_Utils)

if _name and _base:
    # -- Create the new PHX Load, Schedule and Lighting object
    phx_lighting_load = PHX.programs.loads.Load_Lighting()
    phx_lighting_load.name = "LOAD_{}".format(_name)
    phx_lighting_load.target_lux = illumination_level_ or 0
    phx_lighting_load.target_lux_height = illumination_height_ or 0
    phx_lighting_load.watts_per_area = _base.watts_per_area or 0
    
    #-- Add the PHX Load_Lighting to the HB-Lighting
    lighting_ = _base.duplicate()
    lighting_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(lighting_,
                        phx_lighting_load.to_dict(), 'load_lighting', _write_mode='overwrite')
    
    PyPH_Rhino.gh_utils.object_preview(phx_lighting_load)