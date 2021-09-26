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
Occupancy parameters for each Honeybee room. Note that for the inputs, these values
should be PER-HB-ROOM. If a single  value is input, this will be applied for all 
HB-rooms. If a list is input, the values from the list will be applied to the HB-rooms 
in that same order. 
-----
-
EM August 19, 2021
    Args:
        
        num_bedrooms_: (int) For residential only: Enter the number of bedrooms in
            each Honeybee Room. (Note: For PHIUS, Studio apts = 0 Br, 1 occupant)
            If a single value is input, this will be applied to all HB-rooms. If a list is input, the values 
            from the list will be applied to the HB-rooms in order. If none are input, default=1
        
        num_occupants_: (int) For non-residential or multi-unit residential, enter 
            the annual average occpant quantity for each Honeybee Room input. If a single
            value is input, this will be applied to all HB-rooms. If a list is input, the values 
            from the list will be applied to the HB-rooms in order. If none are input, default=None
        
        num_dwelling_units_: (int) For multi-unit residential ONLY. Enter the number of 
            dwelling units in each Honeybee Room input. If a list is input, the values 
            from the list will be applied to the HB-rooms in that order. For single-family
            home, or for Non-Residential zones, leave this input empty.
        ----------
        _HB_rooms: The Honeybee rooms to apply the occupancy parameters to.
    Returns:
        HB_rooms_: The Honeybee rooms with a new Zone-Occupancy applied applied.
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

import PyPH_Rhino.gh_io
import LBT_Utils
import PHX
import PHX.programs.occupancy

# --
import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Zone Occupancy"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="AUG 19, 2021")

if DEV:
    reload(PyPH_Rhino.gh_io)
    reload(LBT_Utils)
    reload(PHX.programs.occupancy)
    reload(PHX.serialization.to_dict)
    reload(PHX.serialization.from_dict)

# Go through and set the occupancy on each HB room, try and get i from list,
# if none input, default to the first one in the list of inputs


def clean_get(IGH, _in, _i, _default=None):
    # type: (IGH, list, int, Any) -> None
    """
    Allow list inputs, if it can, use the current list index
    otherwise, try and use th first list input.  If none, return default
    """

    try:
        input = _in[i]
    except IndexError:
        try:
            input = _in[0]
        except IndexError:
            input = _default

    return PyPH_Rhino.gh_io.input_to_int(IGH, input, _default)


# -- GH Interface
IGH = PyPH_Rhino.gh_io.IGH(ghdoc, ghenv, sc, rh, rs, ghc, gh)

HB_rooms_ = []
for i, room in enumerate(_HB_rooms):
    if not room:
        continue

    new_hb_room = room.duplicate()

    # -- Build a new occupancy object
    occupancy = PHX.programs.occupancy.ZoneOccupancy()

    # -- Get the input data
    occupancy.num_bedrooms = clean_get(IGH, num_bedrooms_, i, 1)
    occupancy.num_occupants = clean_get(IGH, num_occupants_, i, 0)
    occupancy.num_dwelling_units = clean_get(IGH, num_dwelling_units_, i, 0)

    # -- Add the occupancy dict to the HB-Room
    occ_dict = occupancy.to_dict()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(
        new_hb_room, occ_dict, "zone_occupancy", _write_mode="overwrite"
    )

    HB_rooms_.append(new_hb_room)
