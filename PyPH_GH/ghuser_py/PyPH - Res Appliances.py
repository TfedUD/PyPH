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
Calculate lighting and electrical (MEL) loads according to the PHIUS Multifamily 
Calculator (Floor Method).
-----
-
EM August 19, 2021
    Args:
        
        use_PHIUS_defaults_: (bool) If True, will add the 'standard' PHIUS residential 
            appliance set to each honeybee room.
        lighting_exterior_: (kWh/yr) A value or list of values to apply to the Honybee rooms.
        lighting_interior_: (kWh/yr) A value or list of values to apply to the Honybee rooms.
        lighting_garage_: (kWh/yr) A value or list of values to apply to the Honybee rooms.
        mel_: (kWh/yr) A value or list of values to apply to the Honybee rooms.
        _HB_rooms: The Honeybee Rooms to set the appliance values on.
    Returns:
        HB_rooms_: The Honeybee Rooms
"""

import PHX.appliances
import LBT_Utils
import PHX.serialization.to_dict

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Res Appliances"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='AUG 19, 2021')

if DEV:
    reload(PHX.appliances)
    reload(LBT_Utils)
    reload(PHX.serialization.to_dict)

def clean_get(_in, _i, _default=None):
    #type: (list, int, Any) -> None
    """
    Allow list inputs, if it can, use the current list index
    otherwise, try and use the first list input.  If none, return default
    """
    
    try:
        input = _in[i]
    except IndexError:
        try:
            input = _in[0]
        except IndexError:
            input = _default
    
    return input

HB_rooms_ = []
for i, room in enumerate(_HB_rooms):
    if not room: continue
    
    # -- Build the Appliances
    # --------------------------------------------------------------------------
    appliances = PHX.appliances.ApplianceSet()
    # -- Setup the PHIUS appliances
    if use_PHIUS_defaults_:
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Dishwasher())
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Clothes_Washer())
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Clothes_Dryer())
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Cooktop())
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Combo_Fridge())
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Lighting_Int())
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Lighting_Ext())
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_MEL())
    
    
    if lighting_interior_: 
        kwargs = {  'user_defined_total':clean_get(lighting_interior_, i, 0),
                    'reference_quantity':5 ,
                    'energy_demand':100,
                    'energy_demand_per_use':100,
                  }
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Lighting_Int(**kwargs))
    
    if lighting_exterior_: 
        kwargs = {  'user_defined_total':clean_get(lighting_exterior_, i, 0),
                    'reference_quantity':5 ,
                    'energy_demand':100,
                    'energy_demand_per_use':100,
                  }
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_Lighting_Ext(**kwargs))
    
    if mel_: 
        kwargs = {  'user_defined_total':clean_get(mel_, i, 0),
                    'reference_quantity':5 ,
                    'energy_demand':100,
                    'energy_demand_per_use':100,
                  }
        appliances.add_appliance(PHX.appliances.Appliance.PHIUS_MEL(**kwargs))
    
    
    # -- Pack Appliances onto the Room(s)
    # --------------------------------------------------------------------------
    new_hb_room = room.duplicate()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    appliances.to_dict(), 'zone_appliances', _write_mode='overwrite')
    
    HB_rooms_.append(new_hb_room)