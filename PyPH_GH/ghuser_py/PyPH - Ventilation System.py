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
EM August 25, 2021
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
import PHX.hvac
import PHX.ventilation_components

import LBT_Utils

import PyPH_Rhino.ventilation_io
import PyPH_Rhino.gh_io

import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Ventilation System"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="AUG 25, 2021")

if DEV:
    reload(PHX)
    reload(PHX.spaces)
    reload(PHX.hvac)
    reload(PHX.ventilation_components)
    reload(LBT_Utils)
    reload(PHX.serialization)
    reload(PHX.serialization.to_dict)
    reload(PyPH_Rhino.ventilation_io)
    reload(PyPH_Rhino.gh_io)


# -- Interface Object
# -------------------------------------------------------------------------------
IGH = PyPH_Rhino.gh_io.IGH(ghdoc, ghenv, sc, rh, rs, ghc, gh)


# -- Build the new Vent System
# -------------------------------------------------------------------------------
new_system = PHX.ventilation_components.Ventilation_System.default()
new_system.name = system_name_ or "Unnamed Ventilation System"

new_system.ventilator = vent_unit_ or PHX.ventilation_components.Ventilator.default()
new_system.duct_01 = PyPH_Rhino.ventilation_io.handle_duct_input(IGH, duct_01_, "duct_01_")
new_system.duct_02 = PyPH_Rhino.ventilation_io.handle_duct_input(IGH, duct_02_, "duct_02_")


# -- Add the HVAC-System to the Honeybee-Rooms
# -------------------------------------------------------------------------------
HB_rooms_ = []
for hb_room in _HB_rooms:
    new_hb_room = hb_room.duplicate()

    # -- Reset the Ventilator on each of the Spaces, Floors, FloorSegments
    spaces_dict = {}
    for space_dict in hb_room.user_data.get("phx", {}).get("spaces", {}).values():
        # -- Deserialize each space, modify the property
        space_obj = PHX.spaces.Space.from_dict(space_dict)
        space_obj.ventilation.system = new_system

        # -- Reserialize each space
        spaces_dict.update({id(space_obj): space_obj.to_dict()})

    # -- Add the modified spaces nto the new room
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(
        new_hb_room, spaces_dict, "spaces", _write_mode="overwrite"
    )

    # -- Add the System level info as well
    # system_dict = new_system.to_dict()
    # new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
    # system_dict, 'hvac_sys_vent', _write_mode='overwrite')

    HB_rooms_.append(new_hb_room)
