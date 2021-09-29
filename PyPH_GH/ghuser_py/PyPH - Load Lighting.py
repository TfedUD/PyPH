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
TBD
-----
-
EM September 28, 2021
    Args:
        illumination_level_: (lux) The lux target at the illumination plane.
        illumination_height_: (m) The height of the target illumination plane
            above floor level.
    Returns:
        lighting_: 
"""

import PHX
import PHX.programs.loads
import PHX.programs.lighting
import PHX.programs.schedules
import PyPH_Rhino.gh_utils
import LBT_Utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Load Lighting"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='SEP_28_2021')

if DEV:
    reload(PHX.programs.loads)
    reload(PHX.programs.lighting)
    reload(PHX.programs.schedules)
    reload(PyPH_Rhino.gh_utils)
    reload(LBT_Utils)

if _name and _base:
    # -- Create the new PHX Load, Schedule and Lighting object
    phx_lighting_load = PHX.programs.loads.Load_Lighting()
    phx_lighting_load.name = "LOAD_{}".format(_name)
    phx_lighting_load.space_illumination = illumination_level_ or 0
    phx_lighting_load.installed_power_density = illumination_height_ or 0
    
    phx_lighting = PHX.programs.lighting.SpaceLighting()
    phx_lighting.name = _name
    if _base.schedule.user_data:
        phx_lighting.schedule = PHX.programs.schedules.Schedule_Lighting.from_dict(_base.schedule.user_data.get('phx', {}).get('schedule', {}))
    phx_lighting.loads = phx_lighting_load
    
    
    #-- Add the PHX SpaceLighting to the HB-Lighting
    lighting_ = _base.duplicate()
    lighting_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(lighting_,
                        phx_lighting.to_dict(), 'lighting', _write_mode='overwrite')

PyPH_Rhino.gh_utils.object_preview(phx_lighting)