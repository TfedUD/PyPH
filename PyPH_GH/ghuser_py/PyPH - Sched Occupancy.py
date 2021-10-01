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
EM September 28, 2021
    Args:
        start_hour_: (hour) 1-24. default=0 (midnight)
        end_hour_: (hour) 1-24. default = 24 (midnight)
        annual_use_days_: (days) 1-365. default = 365
        absence_factor_: (float 0-1) The average abscence percentage relative
            to the peak / design occupancy for the operating period definded above.
            (0-100%) | 0=occupants never absent, 1=occupants always absent.
        
        illumination_level_: (lux) The lux target at the illumination plane.
        illumination_height_: (m) The height of the target illumination plane
            above floor level.
    Returns:
        HB_occupancy_sched_: 
"""

import LBT_Utils.hb_schedules
import PHX
import PHX.programs.schedules
import PyPH_Rhino.occupancy
import PyPH_Rhino.gh_utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Sched Occupancy"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='SEP_28_2021')

if DEV:
    reload(LBT_Utils.hb_schedules)
    reload(PHX.programs.schedules)
    reload(PyPH_Rhino.occupancy)
    reload(PyPH_Rhino.gh_utils)
    
if _name:
    # -- Create the PHX Occupancy Schedules
    phx_occupancy_schedule = PHX.programs.schedules.Schedule_Occupancy()
    phx_occupancy_schedule.start_hour = start_hour_ or 0
    phx_occupancy_schedule.end_hour = end_hour_ or 24
    phx_occupancy_schedule.annual_utilization_days = annual_use_days_ or 0
    phx_occupancy_schedule.relative_utilization_factor = 1 - (absence_factor_ or 0.0)
    
    
    # -- Create the HB Occupancy Schedule
    HB_occupancy_sched_ = LBT_Utils.hb_schedules.create_hb_constant_schedule(_name, _value=phx_occupancy_schedule.annual_utilization_factor)
    
    # -- Add the PHX Occupancy to the HB Occucpancy
    HB_occupancy_sched_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(HB_occupancy_sched_, 
                         phx_occupancy_schedule.to_dict(), 'schedule', _write_mode='overwrite')
    
    # -- Preview
    PyPH_Rhino.gh_utils.object_preview(phx_occupancy_schedule)