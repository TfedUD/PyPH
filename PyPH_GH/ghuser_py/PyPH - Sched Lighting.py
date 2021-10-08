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
Create a new Honeybee Lighting Schedule based on Passive House Style inputs.
-----
-
EM October 07, 2021
    Args:
        _name: (str) The name to give to the new Honeybee Schedule
        daily_use_hours_: (float) default=24 Number of hours per day that the lighting 
            is operational.
        annual_use_days_: (float) default=365 Number of days per year that the lighting
            is operational.
        relative_utilization_factor_: (float 0.0-1.0) default=1.0 The utilization rate for the operating period
            defined above. Only use this input if you have defined an operating period 
            using daily_use_hours and annual_use_days. If you are trying to simply set
            the annual utilization factor, use the input below and leave this blank.
        annual_utilization_factor_: (float 0.0-1.0) The annual average lighting usage level
            (0-100%) relative to the peak / design lighting level. If you input a value here, 
            it will set the daily_use_hours to 24, and the annual_use_days to 365.
    
    Returns:
        HB_lighting_sched_: The new Honeybee Occupancy Schedule with attributes
            based on the Passive House style inputs. This schedule can be applied to 
            honeybee rooms directly, using the 'HB Apply Room Schedules' component, or
            used to create a Program by connecting it to am 'HB Lighting' component in
            the '_schedule' input.
"""

import PHX.programs.schedules
import PyPH_Rhino.gh_utils
import LBT_Utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Sched Lighting"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_07_2021')

if DEV:
    reload(PHX.programs.schedules)
    reload(PyPH_Rhino.gh_utils)
    reload(LBT_Utils)

if _name:
    # -- Create the PHX Scheduled
    phx_lighting_schedule = PHX.programs.schedules.Schedule_Lighting()
    phx_lighting_schedule.name = _name
    phx_lighting_schedule.daily_operating_hours = daily_use_hours_ or 24
    phx_lighting_schedule.annual_utilization_days = annual_use_days_ or 365
    phx_lighting_schedule.relative_utilization_factor = relative_utilization_factor_ or 1
    phx_lighting_schedule.annual_utilization_factor = annual_utilization_factor_
    
    # -- Create the HB Occupancy Schedule
    HB_lighting_sched_ = LBT_Utils.hb_schedules.create_hb_constant_schedule(_name, _value=phx_lighting_schedule.annual_utilization_factor)
    
    # -- Add the PHX sched data to the HB Object
    HB_occupancy_sched_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(HB_lighting_sched_,
                        phx_lighting_schedule.to_dict(), 'schedule_lighting', _write_mode='overwrite')
    
    # -- Preview
    PyPH_Rhino.gh_utils.object_preview(phx_lighting_schedule)