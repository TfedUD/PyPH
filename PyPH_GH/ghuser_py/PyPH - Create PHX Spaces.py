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
Builds new PHX-Spaces within the Honyebee-Rooms/Zones.
-
EM September 28, 2021
    Args:
        _floor_surfaces (list[Surface]) The individual space floor surfaces represting 
            each individual 'space' inside the Honeybee Room (zone).
        _space_geometry: (list[PolySurface]) Geometry representing the 'space shape' 
            of an individial 'space' or area inside of the Honeybee Room. NOTE: Make 
            sure that your space-shapes are 'open' on the bottom so that they can be 
            joined to the TFA Surfaces to form a closed Brep in the end.
        _HB_rooms:  The Honeybee Rooms you would like to build the PHX-Spaces for.
        _ventilation_rates: Enter either:
"1-Honeybee"
"2-User-Determined"
    Returns:
        floor_surface_breps_: Preview of the Floor Surfaces found / used in the PHX-Spaces
        volume_geometry_breps_: Preview of the PHX-Volume Geometry found/used in the PHX-Spaces
        HB_rooms_: The Honeybee Rooms with new PHX-Spaces added
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

import LBT_Utils

import PHX
import PHX._base
import PHX.hvac_system
import PHX.hvac_components
import PHX.geometry
import PHX.spaces
import PHX.serialization.to_dict
import PHX.serialization.from_dict
import PHX.programs.loads

import PyPH_Rhino
import PyPH_Rhino.gh_io
import PyPH_Rhino.gh_utils
import PyPH_Rhino.spaces
import PyPH_Rhino.space_floors
import PyPH_Rhino.space_volumes
import PyPH_Rhino.space_io

# ---
import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.name = "PyPH - Create PHX Spaces"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="SEP_28_2021")

if DEV:
    reload(LBT_Utils)

    reload(PHX)
    reload(PHX._base)
    reload(PHX.hvac_system)
    reload(PHX.hvac_components)
    reload(PHX.geometry)
    reload(PHX.spaces)
    reload(PHX.serialization.to_dict)
    reload(PHX.serialization.from_dict)
    reload(PHX.programs.loads)

    reload(PyPH_Rhino)
    reload(PyPH_Rhino.gh_io)
    reload(PyPH_Rhino.gh_utils)
    reload(PyPH_Rhino.spaces)
    reload(PyPH_Rhino.space_floors)
    reload(PyPH_Rhino.space_volumes)
    reload(PyPH_Rhino.space_io)


# -- GH Interface
IGH = PyPH_Rhino.gh_io.IGH(ghdoc, ghenv, sc, rh, rs, ghc, gh)

if "2" in str(_ventilation_rates):
    use_ud_vent_rates = True
else:
    use_ud_vent_rates = False

# -- Main
if len(_HB_rooms) > 0:
    floors_dict, floor_surface_breps_ = PyPH_Rhino.spaces.build_floors(
        IGH, _floor_surfaces, "_floor_surfaces", _HB_rooms, use_ud_vent_rates
    )
    volumes, volume_geometry_breps_ = PyPH_Rhino.spaces.build_volumes(
        IGH, floors_dict, _space_geometry, "_space_geometry"
    )
    space_dict = PyPH_Rhino.spaces.build_space_dict(volumes)

# -- Pack up all the results onto the HB Rooms
HB_rooms_ = []
for hb_room in _HB_rooms:
    if not hb_room:
        continue

    new_hb_room = hb_room.duplicate()

    spaces_dict = {}
    for space in space_dict.get(hb_room.identifier, {}).get("Spaces", []):
        print(" -" * 25)
        PyPH_Rhino.gh_utils.object_preview(space)
        spaces_dict.update({id(space): space.to_dict()})

    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(
        new_hb_room, spaces_dict, "spaces", _write_mode="overwrite"
    )

    HB_rooms_.append(new_hb_room)
