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
This component is used to create a simplified Passive-House Style Ventilation Schedule for 
a Space or HB-Room. Input values here for time of operation and fan speed for HIGH 
| MED | LOW | MINIMUM modes.
> By entering reduction factors, full or reduced ventilation operation modes 
within the utilisation period can be considered. All of these attributes can 
be manually input using the Rhino-Scene PHPP tool 'Set TFA Surface Factor(s)'.
> All time values should add up to 24 hours
-
EM September 14, 2021
    Args:
        _name:
            
        _fan_speed_at_high: Fan Speed factor (in %) in relation to the 'design' volume 
            flow when running at HIGH speed.
        _hours_at_high: Total operation time (in hours) of HIGH SPEED ventilation
            mode in relation to the total.
        
        _fan_speed_at_normal: Fan Speed factor (in %) in relation to the 'design' volume 
            flow when running at NORMAL speed.
        _hours_at_normal: Total operation time (in hours) of NORMAL SPEED ventilation
            mode in relation to the total.
        
        _fan_speed_at_low: Fan Speed factor (in %) in relation to the 'design' volume 
            flow when running at LOW speed.
        _hours_at_low: Total operation time (in hours) of LOW SPEED ventilation
            mode in relation to the total.
        
        _fan_speed_at_minimum: Fan Speed factor (in %) in relation to the 'design' volume 
            flow when running at MINIMUM speed.
        _hours_at_minimum: Total operation time (in hours) of MINIMUM SPEED ventilation
            mode in relation to the total.
        
        _HB_rooms: The Honeybee Rooms, with PHX-Spaces, to apply the new schedules to.

    Returns:
        ventilation_schedule_: The PHX-Ventilation Schedules applied to the Room and Spaces
        HB_rooms_: The Honeybee Room(s) with their Spaces and Ventilation Schedules modified.
"""

import Grasshopper.Kernel as ghK

import LBT_Utils

import PHX.serialization.to_dict
import PHX.serialization.from_dict
import PHX
import PHX._base
import PHX.schedules
import PHX.loads
import PHX.hvac
import PHX.ventilation
import PHX.ventilation_components
import PHX.geometry
import PHX.spaces
import PHX.occupancy
import PHX.lighting

import PyPH_Rhino
import PyPH_Rhino.gh_utils

# --- 
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Apply Vent. Schedule"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='SEP_14_2021')

if DEV:
    reload(PHX.serialization.to_dict)
    reload(PHX.serialization.from_dict)
    reload(LBT_Utils)
    reload(PyPH_Rhino)
    reload(PyPH_Rhino.gh_utils)
    
    reload(PHX)
    reload(PHX._base)
    reload(PHX.schedules)
    reload(PHX.loads)
    reload(PHX.hvac)
    reload(PHX.ventilation)
    reload(PHX.ventilation_components)
    reload(PHX.geometry)
    reload(PHX.spaces)
    reload(PHX.occupancy)
    reload(PHX.lighting)

# -- 
HB_rooms_ = []
if _HB_rooms:
    #-- Create the new Ventilation Schedule
    ventilation_schedule_ = PHX.schedules.Schedule_Ventilation()
    
    ventilation_schedule_.name = _name or 'unnamed schedule'
    
    ventilation_schedule_.utilization_rates.maximum.frac_of_design_airflow = _fan_speed_at_high or 0
    ventilation_schedule_.utilization_rates.maximum.daily_op_sched = _hours_at_high or 0
    
    ventilation_schedule_.utilization_rates.standard.frac_of_design_airflow = _fan_speed_at_normal or 0
    ventilation_schedule_.utilization_rates.standard.daily_op_sched = _hours_at_normal or 0
    
    ventilation_schedule_.utilization_rates.basic.frac_of_design_airflow = _fan_speed_at_low or 0
    ventilation_schedule_.utilization_rates.basic.daily_op_sched = _hours_at_low or 0
    
    ventilation_schedule_.utilization_rates.minimum.frac_of_design_airflow = _fan_speed_at_minimum or 0
    ventilation_schedule_.utilization_rates.minimum.daily_op_sched = _hours_at_minimum or 0
    
    #--- Validate the Inputs
    msg = ventilation_schedule_.validate_total_hours()
    if msg:
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)
    
    
    #-- Add the Ventilation Pattern to all the input HB Rooms
    for room in _HB_rooms:
        new_hb_room = room.duplicate()
        
        spaces_dict = {}
        for space_dict in room.user_data.get('phx', {}).get('spaces', {}).values():
            #-- Update the Space properties
            space_obj = PHX.spaces.Space.from_dict(space_dict)
            space_obj.ventilation.schedule = ventilation_schedule_
            spaces_dict.update( {id(space_obj):space_obj.to_dict()} )
            
        new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                        spaces_dict, 'spaces', _write_mode='overwrite')
        
        HB_rooms_.append(new_hb_room)
    
    PyPH_Rhino.gh_utils.object_preview( ventilation_schedule_ )