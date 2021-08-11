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
Assign Honeybee Rooms to a 'Variant' within the PHX Model. In WUFI, this is used
as the 'Case', while in C3RRO this will be considered the 'Variant'. For PHIUS
projects, use this component to break mixed-use projects into separate residential-case
and non-residential-case variants.
-
EM August 11, 2021
    Args:
        _variant_name: 
        _HB_rooms: 
    Returns:
        HB_rooms_: 
"""

import LBT_Utils
import PyPH_Rhino
import PyPH_Rhino.variants

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Create Variant"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='AUG 11, 2021')

if DEV:
    reload(LBT_Utils)
    reload(PyPH_Rhino)
    reload(PyPH_Rhino.variants)

#-- Build the new Variant Identifier
new_variant = PyPH_Rhino.variants.Variant_Identifier()
new_variant.name = _variant_name or 'default_variant'

#-- Add the Ventilation Pattern to all the input HB Rooms
HB_rooms_ = []
for room in _HB_rooms:
    new_hb_room = room.duplicate()
    
    d = new_variant.to_dict()
    
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    d, 'variant_id', _write_mode='overwrite')
    
    HB_rooms_.append(new_hb_room)