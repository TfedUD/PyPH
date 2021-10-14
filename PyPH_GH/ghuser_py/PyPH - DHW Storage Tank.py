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
Create a new DHW Storage Tank for use as part of a DHW System.
-----
-
EM October 14, 2021
    Args:
        name_: (str) The name of the tank.
        volume_: (float) Liters. default=300 (80 Gallons)
        standby_loses_: (float) W/k default=4
    
    Returns:
        tank_: The new PHX DHW Tank. Add this tank to a new PHX DHW System.
"""

import PHX.mechanicals.equipment
import PyPH_Rhino.gh_utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - DHW Storage Tank"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_14_2021')

if DEV:
    reload(PHX.mechanicals.equipment)
    reload(PyPH_Rhino.gh_utils)
    reload(PHX.serialization.to_dict)
    reload(PHX.serialization.from_dict)

tank_ = PHX.mechanicals.equipment.HW_Tank()
tank_.name = name_ or "_unnamed_water_tank_"
tank_.device_type = 8 # Water storage
tank_.system_type = 8 # Water storage

tank_.properties.volume = volume_ or 300 # Liters = 80 Gallons
tank_.properties.standby_loses = standby_loses_ or 4 # W/k

PyPH_Rhino.gh_utils.object_preview(tank_)