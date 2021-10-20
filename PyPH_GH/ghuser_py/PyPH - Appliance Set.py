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
Set Passive House Appliance and Lighting energy loads on the Honeybee Rooms.
-----
-
EM October 20, 2021
    Args:
        
        use_PHIUS_defaults_: (bool) If True, will add the 'standard' PHIUS residential 
            appliance set to each honeybee room.
            Alternatively pass the string "SF" to set the Single-Family appliance defaults
            or pass the string "MF" to set the Multi-Family appliance defaults (no laundry)
            
        appliances_: (PHX Appliance) A list of user-determiend PHX Appliances to add to the set. Use the 
            "PyPH - Appliance" component to build individial appliances to add to this set.
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
ghenv.Component.Name = "PyPH - Appliance Set"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_20_2021')

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
    appliance_set = PHX.appliances.ApplianceSet()
    # -- Setup the PHIUS appliances
    if str(use_PHIUS_defaults_).upper() == 'MF':
        # Apply the Multi-Family (MF) Default Set
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Dishwasher())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Cooktop())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Combo_Fridge())
    elif use_PHIUS_defaults_ or str(use_PHIUS_defaults_).upper() == 'SF':
        # Apply the Single-Family (SF) Default Set
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Dishwasher())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Clothes_Washer())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Clothes_Dryer())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Cooktop())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Combo_Fridge())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Lighting_Int())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Lighting_Ext())
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_MEL())
    
    # -- Add in the User-Determined Appliances
    # --------------------------------------------------------------------------
    appliance_set.add_appliances_to_set(appliances_)
    
    # -- Lighting and MEL
    # --------------------------------------------------------------------------
    if lighting_interior_:
        appliance_set.remove_type_from_set('PHIUS_Lighting_Int')
        kwargs = {  'type': 17, # "User defined - lighting"
                    'reference_quantity':5,
                    'energy_demand':clean_get(lighting_interior_, i, 0),
                    'comment': 'PHIUS Interior Lighting'
                  }
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.Custom_Electric_per_Year(**kwargs))
    
    if lighting_exterior_:
        appliance_set.remove_type_from_set('PHIUS_Lighting_Ext')
        kwargs = {  'type': 17, # "User defined - lighting"
                    'reference_quantity':5,
                    'energy_demand':clean_get(lighting_exterior_, i, 0),
                    'comment': 'PHIUS Exterior Lighting'
                  }
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.Custom_Electric_per_Year(**kwargs))
    
    if mel_:
        appliance_set.remove_type_from_set('PHIUS_MEL')
        kwargs = {  'type': 18, # "User defined - Misc electric loads"
                    'reference_quantity':5,
                    'energy_demand':clean_get(mel_, i, 0),
                    'comment': 'PHIUS MEL'
                  }
        appliance_set.add_appliances_to_set(PHX.appliances.Appliance.Custom_Electric_per_Year(**kwargs))
    
    
    # -- Pack Appliances onto the Room(s)
    # --------------------------------------------------------------------------
    new_hb_room = room.duplicate()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    appliance_set.to_dict(), 'zone_appliances', _write_mode='overwrite')
    
    HB_rooms_.append(new_hb_room)