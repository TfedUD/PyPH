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
Collects and organizes data for a simple fresh-air ventilation system (HRV/ERV). 
Outputs a 'ventilation' class object to apply to a HB Zone.
-
EM October 05, 2021
    Args:
        system_name_: <Optional> A name for the overall system. ie: 'ERV-1', 
            etc.. Will show up in the 'Additional Ventilation' worksheet as the 
            'Description of Ventilation Units' (E97-E107)
        system_type_: Input Type. Either: "1-Balanced PH ventilation with HR
            [Default]", "2-Extract air unit", "3-Only window ventilation"
        vent_unit_: Input the HRV/ERV unit object. Connect to the 'ventUnit_' 
            output on the 'Ventilator' Component
        duct_01_: Input the HRV/ERV Duct object. Connect to the 'hrvDuct_' 
            output on the 'Vent Duct' Component
        duct_02_: Input the HRV/ERV Duct object. Connect to the 'hrvDuct_' 
            output on the 'Vent Duct' Component
    Returns:
        HB_rooms_: The Honeybee Room(s) with their PHX-Space Ventilation values modified.
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

import PHX
import PHX.spaces
import PHX.mechanicals.systems
import PHX.mechanicals.equipment
import PHX.mechanicals.distribution
import LBT_Utils

import PyPH_Rhino.ventilation
import PyPH_Rhino.gh_io
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
from System import Object


import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Ventilation System"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_05_2021')

if DEV:
    reload(PHX)
    reload(PHX.spaces)
    reload(PHX.mechanicals.systems)
    reload(PHX.mechanicals.equipment)
    reload(PHX.mechanicals.distribution)
    reload(LBT_Utils)
    reload(PHX.serialization)
    reload(PHX.serialization.to_dict)
    reload(PyPH_Rhino.ventilation) 
    reload(PyPH_Rhino.gh_io)


def default_list_item(_list, _branch_num):
    #type: (list, int) -> Any
    """Try and return default list item if IndexError"""
    
    if not _list:
        return None
    
    try:
        return _list[_branch_num]
    except IndexError as e:
        
        return _list[0]

#-- Interface Object
#-------------------------------------------------------------------------------
IGH = PyPH_Rhino.gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )


#-- Build the new Vent System
#-------------------------------------------------------------------------------
HB_rooms_ = DataTree[Object]()
for i, branch in enumerate(_HB_rooms.Branches):
    
    new_system = PHX.mechanicals.systems.MechanicalSystem()
    new_system.name = default_list_item(system_name_, i) or 'Unnamed Ventilation System'
    
    vent_unit = default_list_item(vent_unit_, i) or PHX.mechanicals.equipment.HVAC_Ventilator()
    new_system.equipment_set.add_new_device_to_equipment_set( vent_unit )
    #new_system.duct_01 = PyPH_Rhino.ventilation.create_duct(IGH, duct_01_, 'duct_01_')
    #new_system.duct_02 = PyPH_Rhino.ventilation.create_duct(IGH, duct_02_, 'duct_02_')
    
    
    #-- Add the HVAC-System to the Honeybee-Rooms
    #-------------------------------------------------------------------------------
    #branch_HB_rooms_ = []
    for hb_room in branch:
        new_hb_room = hb_room.duplicate()
        
        # -- Add the Mechanical System to the Room
        new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                        new_system.to_dict(), 'mechanicals', _write_mode='overwrite')
        
        HB_rooms_.Add( new_hb_room, GH_Path(i) )
    
    PyPH_Rhino.gh_utils.object_preview(new_system)