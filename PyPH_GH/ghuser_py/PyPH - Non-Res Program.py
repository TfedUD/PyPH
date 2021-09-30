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
Sets up the Non-Residential attributes needed for Passive House models. In WUFI passive
these attributes are set in the "Internal Loads/Occupancy" tab when 'Non-Residential' is 
set as the building type at the 'Case' level.
-----
-
EM August 26, 2021
    Args:
        start_hour_: (hour) 1-24. default=1
        end_hour_: (hour) 1-24. default = 24
        annual_use_days_: (days) 1-365. default = 365
        occupancy_factor_: (float 0-1) The annual average occupancly level (0-100%) relative
            to the peak / design occupancy.
        
        illumination_level_: (lux) The lux target at the illumination plane.
        illumination_height_: (m) The height of the target illumination plane
            above floor level.
        lighting_use_factor_: (float 0-1) The annual average lighting usage level
            (0-100%) relative to the peak / design lighting level.
        
        ----------
        _HB_rooms: The Honeybee rooms to apply the occupancy and lighting parameters to.
    Returns:
        HB_rooms_: The Honeybee rooms with a new Space-Occupancy and lighting applied.
"""


import PHX
import PHX.spaces
import LBT_Utils
import LBT_Utils.hb_schedules
import PyPH_Rhino.occupancy
import PyPH_Rhino.lighting

# --
import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.name = "PyPH - Non-Res Program"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="AUG 26, 2021")

if DEV:
    reload(PHX)
    reload(PHX.spaces)
    reload(LBT_Utils)
    reload(LBT_Utils.hb_schedules)
    reload(PyPH_Rhino.occupancy)
    reload(PHX.utilization_patterns)
    reload(PyPH_Rhino.lighting)


# -- Set the Occpancy and Lighting on the spaces
HB_rooms_ = []
for room in _HB_rooms:
    if not room:
        continue
    new_hb_room = room.duplicate()

    #
    #
    #
    # TODO: GH User inputs
    #
    #
    #

    # -- Calc a new PHX Style occupancy from the HB Room
    hb_occ = room.properties.energy.people
    hb_lighting = room.properties.energy.lighting
    new_phx_occupany = PyPH_Rhino.occupancy.phx_occupancy_from_hb(hb_occ)
    new_phx_lighting = PyPH_Rhino.lighting.phx_lighting_from_hb(hb_lighting)

    # -- Build a new Occupancy based on the HB Zone,
    # -- Apply it to each space in the Zone
    space_dicts = room.user_data.get("phx", {}).get("spaces", {})
    new_spaces = []
    for space_dict in space_dicts.values():
        new_space = PHX.spaces.Space.from_dict(space_dict)
        new_space.occupancy = new_phx_occupany
        new_space.lighting = new_phx_lighting
        new_spaces.append(new_space)

    # -- pack new dict onto HB Room
    space_dict = {id(space): space.to_dict() for space in new_spaces}
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(
        new_hb_room, space_dict, "spaces", _write_mode="overwrite"
    )

    HB_rooms_.append(new_hb_room)
