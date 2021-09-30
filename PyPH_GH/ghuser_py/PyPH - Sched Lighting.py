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
TBD
-----
-
EM September 28, 2021
    Args:
        annual_utilization_fac_: (float 0-1) The annual average lighting usage level
            (0-100%) relative to the peak / design lighting level.
    Returns:
        HB_occupancy_sched_: 
"""

import PHX.programs.schedules
import PyPH_Rhino.gh_utils
import LBT_Utils

# --
import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.name = "PyPH - Sched Lighting"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="SEP_28_2021")

if DEV:
    reload(PHX.programs.schedules)
    reload(PyPH_Rhino.gh_utils)
    reload(LBT_Utils)

if _name:
    # -- Create the PHX Scheduled
    phx_lighting_schedule = PHX.programs.schedules.Schedule_Lighting()
    phx_lighting_schedule.name = _name
    phx_lighting_schedule.annual_utilization_factor = annual_utilization_fac_ or 1

    # -- Create the HB Occupancy Schedule
    HB_lighting_sched_ = LBT_Utils.hb_schedules.create_hb_constant_schedule(
        _name, _value=phx_lighting_schedule.annual_utilization_factor
    )

    # -- Add the PHX sched data to the HB Object
    HB_occupancy_sched_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(
        HB_lighting_sched_, phx_lighting_schedule.to_dict(), "schedule", _write_mode="overwrite"
    )

    # -- Preview
    PyPH_Rhino.gh_utils.object_preview(phx_lighting_schedule)
