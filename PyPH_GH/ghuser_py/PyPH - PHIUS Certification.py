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
-
EM October 05, 2021
    Args:
        bldg_status_: Input either -
            "1-In planning" (default)
            "2-Under construction"
            "3-Completed"
        
        bldg_type_: Input either -
            "1-New construction" (default)
            "2-Retrofit"
            "3-Mixed - new construction/retrofit"
    Returns:
        certification_:
"""

import PHX.bldg_segment
import PyPH_Rhino.gh_utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - PHIUS Certification"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_05_2021')

if DEV:
    reload(PHX.bldg_segment)
    reload(PyPH_Rhino.gh_utils)

certification_ = PHX.bldg_segment.PHIUSCertification()


certification_.PHIUS2021_heating_demand = _PHIUS_annual_heating_demand_kWh_m2 or 15
certification_.PHIUS2021_cooling_demand = _PHIUS_annual_cooling_demand_kWh_m2 or 15
certification_.PHIUS2021_heating_load = _PHIUS_peak_heating_load_W_m2 or 10
certification_.PHIUS2021_cooling_load = _PHIUS_peak_cooling_load_W_m2 or 10

certification_.building_status = bldg_status_ or 1  # In Planning
certification_.building_type = bldg_type_ or 1  # New Construction

PyPH_Rhino.gh_utils.object_preview(certification_)