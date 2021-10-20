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
Configure the WUFI / PHPP Program options, including Climate and Program settings.
-
EM October 20, 2021
    Args:
        _climate: The PHX Climate to apply to the Builing Segments.
        
        _HB_model: The Honeybee Model.
    
    Returns:
        HB_Model_: The Honeybee Model with PHX Configuration settings applied.
"""

import PHX.climate
import PHX.serialization.from_dict
import PHX.serialization.to_dict
import LBT_Utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - WUFI Config"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_19_2021')

if DEV:
    reload(LBT_Utils)
    reload(PHX.climate)
    reload(PHX.serialization.from_dict)
    reload(PHX.serialization.to_dict)


if _HB_model:
    HB_Model_ = _HB_model.duplicate()
    
    if _climate:
        climate_dict = _climate.to_dict()
        HB_Model_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(HB_Model_,
                                        climate_dict, 'climate', _write_mode='overwrite')