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
EM September 28, 2021
    Args:
        
        lighting_frac_HE_ext_: (float) Fraction of the exterior lighting which is 'high efficiency'
        lighting_frac_HE_int_: (float) Fraction of the interior lighting which is 'high efficiency'
        lighting_frac_HE_garage_: (float) Fraction of the garage lighting which is 'high efficiency'
        _HB_rooms: (Honeybee Rooms): The Honeybee Rooms to calculate the values for
    Returns:
        lighting_exterior_: (kWh/dwelling-unit) Pass these values to a PHX Appliances component to set the values.
        lighting_interior_: (kWh/dwelling-unit) Pass these values to a PHX Appliances component to set the values.
        lighting_garage_: (kWh/dwelling-unit) Pass these values to a PHX Appliances component to set the values.
        mel_: (kWh/dwelling-unit) Pass these values to a PHX Appliances component to set the values.
        HB_rooms_: The Honeybee Rooms
        ----
        non_res_spaces_: For PHIUS Multifamily calculator. Copy/Paste values to spreadsheet
        non_res_space_types_: For PHIUS Multifamily calculator. Copy/Paste values to spreadsheet
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh


import PHX.programs.occupancy
import PyPH_Rhino.phius_MF_electric
import PyPH_Rhino.gh_io

# --
import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.name = "PyPH - PHIUS MF Calculator"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="SEP_28_2021")

if DEV:
    reload(PHX.programs.occupancy)
    reload(PyPH_Rhino.phius_MF_electric)
    reload(PyPH_Rhino.gh_io)

# -- GH Interface
IGH = PyPH_Rhino.gh_io.IGH(ghdoc, ghenv, sc, rh, rs, ghc, gh)

lighting_exterior_ = []
lighting_interior_ = []
lighting_garage_ = []
mel_ = []
non_res_spaces_ = []
non_res_space_types_ = []
space_types_dict = {}
HB_rooms_ = []

stories_dict = PyPH_Rhino.phius_MF_electric.sort_rooms_by_story(_HB_rooms)
for room_list in stories_dict.values():
    # -- Filter Residential Rooms from Non-Residential
    non_res_rooms = []
    res_rooms = []
    for room in room_list:
        room_occupancy = PHX.programs.occupancy.ZoneOccupancy.from_dict(
            room.user_data.get("phx", {}).get("zone_occupancy", {})
        )
        if room_occupancy.num_dwelling_units > 0:
            res_rooms.append(room)
        else:
            non_res_rooms.append(room)

    # -- Calc Non-Residential Values
    for room in non_res_rooms:
        # -- Calculate all values using Honeybee Program first
        lighting = PyPH_Rhino.phius_MF_electric.hb_lighting_values(room)
        mel = PyPH_Rhino.phius_MF_electric.hb_mel_values(room)

        # -- For PHIUS MF Spreadsheet
        room_type = room.properties.energy.program_type.display_name
        space_types_dict[room_type] = (
            room_type,
            lighting.util_day_per_yr,
            lighting.daily_operating_hrs,
            lighting.w_sf,
            mel.kWh_sf_yr,
        )

        results = PyPH_Rhino.phius_MF_electric.annual_lighting_and_mel(room, lighting, mel)
        lighting_exterior_.append(0)
        lighting_interior_.append(results.lighting_annual_kWh)
        lighting_garage_.append(0)
        mel_.append(results.mel_annual_kWh)
        non_res_spaces_.extend(results.spaces)

        HB_rooms_.append(room)

    # -- Calculate Residential Values
    attrs = PyPH_Rhino.phius_MF_electric.get_room_attributes(res_rooms)

    l_ext = PyPH_Rhino.phius_MF_electric.story_lighting_exterior(
        attrs.m2_per_unit, attrs.num_dwelling_units, lighting_frac_HE_ext_
    )
    l_int = PyPH_Rhino.phius_MF_electric.story_lighting_interior(
        attrs.m2_per_unit, attrs.num_dwelling_units, lighting_frac_HE_int_
    )
    l_gar = PyPH_Rhino.phius_MF_electric.story_lighting_garage(attrs.num_dwelling_units, lighting_frac_HE_garage_)
    mel = PyPH_Rhino.phius_MF_electric.story_mel(attrs.m2_per_unit, attrs.num_dwelling_units, attrs.num_bedrooms)

    for room in res_rooms:
        lighting_exterior_.append(l_ext / attrs.num_dwelling_units)
        lighting_interior_.append(l_int / attrs.num_dwelling_units)
        lighting_garage_.append(l_gar / attrs.num_dwelling_units)
        mel_.append(mel / attrs.num_dwelling_units)

        HB_rooms_.append(room)


# -- For PHIUS MF Calculator Spreadsheet
for k, v in space_types_dict.items():
    non_res_space_types_.append("{},{},{},{},{}".format(*v))
