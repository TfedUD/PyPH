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
EM August 13, 2021
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
        num_of_floor_levels_: Total number of floor levels in this building-segment
        num_units_: Total number of 'units'. For residential, this is the number of
            dwelling units. For non-residential, leave this set to "1".
        bldg_status_: Input either -
            "1-In planning" (default)
            "2-Under construction"
            "3-Completed"
        bldg_type_: Input either -
            "1-New construction" (default)
            "2-Retrofit"
            "3-Mixed - new construction/retrofit"
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
import PHX
import PHX.bldg_segment
import PHX.occupancy
import PyPH_Rhino.gh_io
import PyPH_Rhino.bldg_segment_id
import PyPH_Rhino.io_bldg_segment

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Create Bldg Segment"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='AUG 13, 2021')

if DEV:
    reload(LBT_Utils)
    reload(PHX.serialization.to_dict)
    reload(PHX.bldg_segment)
    reload(PHX.occupancy)
    reload(PyPH_Rhino.gh_io)
    reload(PyPH_Rhino.bldg_segment_id)
    reload(PyPH_Rhino.io_bldg_segment)

# -- GH Interface
IGH = PyPH_Rhino.gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

#--
new_bldg_segment = PyPH_Rhino.bldg_segment_id.BldgSegment_ID()
new_bldg_segment.name = segment_name_ or '_default_building_'

# --
new_segment_occupancy = PHX.occupancy.BldgSegmentOccupancy()
new_segment_occupancy.usage_type = PyPH_Rhino.gh_io.input_to_int(IGH, usage_type_, 1)
new_segment_occupancy.category = PyPH_Rhino.gh_io.input_to_int(IGH, occupancy_category_, 1)
new_segment_occupancy.num_stories = PyPH_Rhino.gh_io.input_to_int(IGH, num_of_floor_levels_, 1)
new_segment_occupancy.num_units = PyPH_Rhino.gh_io.input_to_int(IGH, num_units_, 1)
IGH.warning(new_segment_occupancy.validate())

#-- PH Params
new_PH_params = PHX.bldg_segment.PHIUSCertification()
new_PH_params.building_status = PyPH_Rhino.gh_io.input_to_int(IGH, bldg_status_, 1)
new_PH_params.building_type = PyPH_Rhino.gh_io.input_to_int(IGH, bldg_type_, 1)


#-- Add the data to all the input HB Rooms
HB_rooms_ = []
for room in _HB_rooms:
    new_hb_room = room.duplicate()
    
    bldg_seg_dict = new_bldg_segment.to_dict()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    bldg_seg_dict, 'bldg_segment_id', _write_mode='overwrite')
    
    occ_dict = new_segment_occupancy.to_dict()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    occ_dict, 'occupancy', _write_mode='overwrite')
    
    ph_param_dict = new_PH_params.to_dict()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                    ph_param_dict, 'ph_certification', _write_mode='overwrite')
    
    HB_rooms_.append(new_hb_room)