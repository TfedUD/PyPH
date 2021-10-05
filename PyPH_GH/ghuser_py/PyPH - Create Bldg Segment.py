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
Assign Honeybee Rooms to a specific 'Buildiing Segment' within the PHX Model. In WUFI, this is used
as the 'Case', while in C3RRO this will be considered the 'Variant'. For PHIUS
projects, use this component to break mixed-use projects into separate residential-case
and non-residential-case variants.
-
EM October 05, 2021
    Args:
        segment_name_: Name for the building-segment
        
        occupancy_category_: Input either -
            "1-Residential" (default)
            "2-Non-residential"
        
        usage_type_: Input either -
            "1-Residential" (default)
            "4-Office/Administrative building"
            "5-School"
            "6-Other"
            "7-Undefined/unfinished"
        
        num_of_floor_levels_: (int) Total number of floor levels for the group of 
            Honeybee rooms input. Default=1
        
        num_units_: (int) Total number of 'units' for the group of Honeybee rooms
            input For residential, this is the total number of dwelling units
            in the group of HB-Room. For non-residential, leave this set to "1".
        
        winter_set_temp_: default = 20C [68F]
        
        summer_set_temp_: default = 25C [77F]
        
        ----------
        _HB_rooms: The Honeybee rooms to include in this Building Segment
    
    Returns:
        HB_rooms_: The Honeybee rooms assigned to this Building Segment
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

import LBT_Utils
import LBT_Utils.hb_schedules

import PHX
import PHX.bldg_segment
import PHX.programs.occupancy
import PHX.programs.lighting
import PHX.programs.schedules
import PHX.spaces

import PyPH_Rhino.gh_io
import PyPH_Rhino.bldg_segment_id
import PyPH_Rhino.occupancy
import PyPH_Rhino.lighting
import PyPH_Rhino.gh_utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Create Bldg Segment"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_05_2021')

if DEV:
    reload(LBT_Utils)
    reload(LBT_Utils.hb_schedules)
    reload(PHX.serialization.to_dict)
    reload(PHX.serialization.from_dict)
    reload(PHX.bldg_segment)
    reload(PHX.spaces)
    reload(PHX.programs.occupancy)
    reload(PHX.programs.lighting)
    reload(PHX.programs.schedules)
    reload(PyPH_Rhino.gh_io)
    reload(PyPH_Rhino.bldg_segment_id)
    reload(PyPH_Rhino.occupancy)
    reload(PyPH_Rhino.lighting)

# -- GH Interface
IGH = PyPH_Rhino.gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

#-- New Segment
new_bldg_segment = PyPH_Rhino.bldg_segment_id.BldgSegment_ID()
new_bldg_segment.name = segment_name_ or '_default_building_'

# -- Segment Occupancy
occupancy = PHX.programs.occupancy.BldgSegmentOccupancy()
occupancy.category = PyPH_Rhino.gh_io.input_to_int(IGH, occupancy_category_, 1)
occupancy.usage_type = PyPH_Rhino.gh_io.input_to_int(IGH, usage_type_, 1)
occupancy.num_stories = PyPH_Rhino.gh_io.input_to_int(IGH, num_floor_levels_, 1)
occupancy.num_units = PyPH_Rhino.gh_io.input_to_int(IGH, num_units_, 1)
IGH.warning(occupancy.validate())

#-- PH Params
if _PHIUS_certification:
    new_PH_params = _PHIUS_certification
else:
    new_PH_params = PHX.bldg_segment.PHIUSCertification()

PyPH_Rhino.gh_utils.object_preview(new_bldg_segment)
PyPH_Rhino.gh_utils.object_preview(occupancy)
PyPH_Rhino.gh_utils.object_preview(new_PH_params)

#-- Add the data to all the input HB Rooms
HB_rooms_ = []
for room in _HB_rooms:
    if not room: continue
    new_hb_room = room.duplicate()
    
    # -- NON_RES ONLY
    if occupancy.category == 2:
        default_name = room.properties.energy.program_type.display_name
        # -- For Non-Residential, calc the PHX Occupancy and Lighting Schedules
        hb_occ = room.properties.energy.people
        hb_lighting = room.properties.energy.lighting
        new_phx_occupancy = PyPH_Rhino.occupancy.phx_occupancy_from_hb(hb_occ, default_name)
        new_phx_lighting = PyPH_Rhino.lighting.phx_lighting_from_hb(hb_lighting)
        
        # -- Build a new Occupancy based on the HB Zone,
        # -- Apply it to each space in the Zone
        space_dicts = room.user_data.get('phx',{}).get('spaces',{})
        new_spaces = []
        for space_dict in space_dicts.values():
            new_space = PHX.spaces.Space.from_dict(space_dict)
            new_space.occupancy = new_phx_occupancy
            new_space.lighting = new_phx_lighting
            new_spaces.append(new_space)
            
        # -- pack new dict onto HB Room
        space_dict = {id(space):space.to_dict() for space in new_spaces}
        new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    space_dict, 'spaces', _write_mode='overwrite')
    
    # -- ALL
    #-- Pack everything back into the HB Room user-data
    bldg_seg_dict = new_bldg_segment.to_dict()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    bldg_seg_dict, 'bldg_segment_id', _write_mode='overwrite')
    
    occ_dict = occupancy.to_dict()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    occ_dict, 'segment_occupancy', _write_mode='overwrite')
    
    ph_param_dict = new_PH_params.to_dict()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    ph_param_dict, 'ph_certification', _write_mode='overwrite')
    
    HB_rooms_.append(new_hb_room)