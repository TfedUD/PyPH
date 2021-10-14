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
        name_: (str) The name of the DHW System..
        hot_water_heater_: (Optional) A PHX Hot-Water heater to add as part of the system.
        tank_: (Optional) A PHX DHW Tank to add as part of the system.
        _HB_rooms: The Honeybee rooms to add the DHW system to.
    
    Returns:
        HB_rooms_: The Honeybee rooms with the new DHW system added.
"""


import PHX.mechanicals.distribution
import PHX.mechanicals.equipment
import PHX.mechanicals.systems
import LBT_Utils
import PyPH_Rhino.gh_utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - DHW System"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_14_2021')

if DEV:
    reload( PHX.mechanicals.distribution )
    reload( PHX.mechanicals.equipment )
    reload( PHX.mechanicals.systems )
    reload( LBT_Utils )
    reload( PyPH_Rhino.gh_utils )
    reload(PHX.serialization.from_dict)
    reload(PHX.serialization.to_dict)

# -- Build the new DHW Mechanical System

dhw_system = PHX.mechanicals.systems.MechanicalSystem()
dhw_system.name = name_ or '_unnamed_hot_water_system_'
dhw_system.system_group_type_number = 1
dhw_system.system_usage.used_for_DHW = True

dhw_system.equipment_set.add_new_device_to_equipment_set(hot_water_heater_)
dhw_system.equipment_set.add_new_device_to_equipment_set(tank_)

HB_rooms_ = []
for room in _HB_rooms:
    #-- Add the HVAC-System to the Honeybee-Rooms
    #-------------------------------------------------------------------------------
    new_hb_room = room.duplicate()
    
    # -- Add the Mechanical System to the Room
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    dhw_system.to_dict(), 'mech_system_dhw', _write_mode='overwrite')
    
    HB_rooms_.append( new_hb_room )

PyPH_Rhino.gh_utils.object_preview(dhw_system)
