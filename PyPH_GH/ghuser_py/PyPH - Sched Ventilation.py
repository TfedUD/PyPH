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
a Space or HB-Room.
> Input values here for time of operation and fan speed for HIGH | MED | LOW | MINIMUM modes. 
> Once this schedule is created, either use it as part of a 
Honeybee 'Program' and/or apply it directly to rooms using the Honeybee 'Apply Room Schedules' component.
> Total usage hours/day should add up to 24 hours
-
EM October 01, 2021
    Args:
        _name:
            
        operating_day_per_week_: (default=7) Value for the number of days/week to run
            at the specified flowrates.
        operating_weeks_per_year_: (default=52) Value for the number of weeks/year to 
            run at the specified flowrates.
        
        _fan_speed_at_high: Fan Speed factor (in %) in relation to the 'design' volume
            flow when running at HIGH speed.
        _hours_at_high: Total operation time (in hours/day) of HIGH SPEED ventilation
            mode in relation to the total.
        
        _fan_speed_at_normal: Fan Speed factor (in %) in relation to the 'design' volume 
            flow when running at NORMAL speed.
        _hours_at_normal: Total operation time (in hours/day) of NORMAL SPEED ventilation
            mode in relation to the total.
        
        _fan_speed_at_low: Fan Speed factor (in %) in relation to the 'design' volume 
            flow when running at LOW speed.
        _hours_at_low: Total operation time (in hours/day) of LOW SPEED ventilation
            mode in relation to the total.
        
        _fan_speed_at_minimum: Fan Speed factor (in %) in relation to the 'design' volume 
            flow when running at MINIMUM speed.
        _hours_at_minimum: Total operation time (in hours/day) of MINIMUM SPEED ventilation
            mode in relation to the total.
    
    Returns:
        ventilation_sch_: The HB-Ventilation Schedule which can be applied to HB Rooms
"""

import Grasshopper.Kernel as ghK

import LBT_Utils

import PHX.serialization.to_dict
import PHX.serialization.from_dict
import PHX
import PHX._base
import PHX.programs.schedules
import PHX.programs.loads
import PHX.geometry
import PHX.spaces
import PHX.programs.occupancy
import PHX.programs.lighting

import PyPH_Rhino
import PyPH_Rhino.gh_utils

# --- 
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Sched Ventilation"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_01_2021')

if DEV:
    reload(PHX.serialization.to_dict)
    reload(PHX.serialization.from_dict)
    reload(LBT_Utils)
    reload(PyPH_Rhino)
    reload(PyPH_Rhino.gh_utils)
    
    reload(PHX)
    reload(PHX._base)
    reload(PHX.programs.schedules)
    reload(PHX.programs.loads)
    reload(PHX.geometry)
    reload(PHX.spaces)
    reload(PHX.programs.occupancy)
    reload(PHX.programs.lighting)

#-- Create the new Ventilation Schedule
phx_vent_sched = PHX.programs.schedules.Schedule_Ventilation()

phx_vent_sched.name = _name or 'unnamed schedule'

phx_vent_sched.operating_days = operating_day_per_week_ or 7
phx_vent_sched.operating_weeks = operating_weeks_per_year_ or 52

phx_vent_sched.utilization_rates.maximum.frac_of_design_airflow = _fan_speed_at_high or 0
phx_vent_sched.utilization_rates.maximum.daily_op_sched = _hours_at_high or 0

phx_vent_sched.utilization_rates.standard.frac_of_design_airflow = _fan_speed_at_normal or 0
phx_vent_sched.utilization_rates.standard.daily_op_sched = _hours_at_normal or 0

phx_vent_sched.utilization_rates.basic.frac_of_design_airflow = _fan_speed_at_low or 0
phx_vent_sched.utilization_rates.basic.daily_op_sched = _hours_at_low or 0

phx_vent_sched.utilization_rates.minimum.frac_of_design_airflow = _fan_speed_at_minimum or 0
phx_vent_sched.utilization_rates.minimum.daily_op_sched = _hours_at_minimum or 0

#--- Validate the Inputs
msg = phx_vent_sched.validate_total_hours()
if msg:
    ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)

# -- Create the new HB Vent Sched
ventilation_sch_ = LBT_Utils.hb_schedules.create_hb_constant_schedule(phx_vent_sched.name, _value=phx_vent_sched.annual_utilization_factor)

# -- Add the PHX Vent Sched to the HB Vent Sched
ventilation_sch_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(ventilation_sch_, 
                     phx_vent_sched.to_dict(), 'schedule', _write_mode='overwrite')

PyPH_Rhino.gh_utils.object_preview( phx_vent_sched )