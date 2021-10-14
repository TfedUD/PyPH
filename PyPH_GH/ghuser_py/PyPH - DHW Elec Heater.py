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
Create a new DHW Heating element for use as part of a DHW System.
-----
-
EM October 14, 2021
    Args:
        name_: (str) The name of the tank.
        watts_: (float) The output wattage (max) of the heater. Default=2000
    
    Returns:
        hot_water_heater_: The new PHX DHW Direct Electric heater. 
            Add this heater to a PHX DHW System.
"""

import PHX.mechanicals.equipment
import PyPH_Rhino.gh_utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - DHW Elec Heater"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_14_2021')

if DEV:
    reload(PHX.mechanicals.equipment)
    reload(PyPH_Rhino.gh_utils)
    reload(PHX.serialization.to_dict)
    reload(PHX.serialization.from_dict)

hot_water_heater_ = PHX.mechanicals.equipment.HW_Heater_Direct_Elec()
hot_water_heater_.name = name_ or "_unnamed_water_heater_"
hot_water_heater_.device_type = 2
hot_water_heater_.device_type = 2

hot_water_heater_.properties.watts = watts_ or 2000


PyPH_Rhino.gh_utils.object_preview(hot_water_heater_)