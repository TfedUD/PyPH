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
Collects and organizes data for a Ventilator Unit (HRV/ERV). Used to build up a 
PH-Style Ventilation System.
-
EM October 05, 2021
    Args:
        unit_name_: <Optional> The name of the Ventilator Unit
        heat_recovery_eff_: <Optional> Input the Ventialtion Unit's Heat Recovery %. Default is 75% 
        moisture_recovery_eff_: <Optional> Input the Ventialtion Unit's Moisture Recovery %. Default is 0% (HRV)
        electrical_eff_: <Optional> Input the Electrical Efficiency of the Ventialtion 
            Unit (W/m3h). Default is 0.45 W/m3h
        frost_temp_: Min Temp for frost protection to kick in. [deg.  C]. Default is -5 C
        install_location_: 
    Returns:
        unit_: A Ventilator object for the Ventilation System. Connect to the 
            'ventUnit_' input on the 'Create Vent System' to build a PH-Style Ventilation System.
"""

import PHX.mechanicals.equipment
import PyPH_Rhino.gh_utils

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Ventilation Unit"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_05_2021')

if DEV:
    reload(PHX.mechanicals.equipment)
    reload(PyPH_Rhino.gh_utils)

def validate_efficiency(_in):
    if not _in: return None
    
    if float(_in) > 1:
        return float(_in)/100
    else:
        return float(_in)

def default_list_item(_list, _index):
    #type: (list, int) -> Any
    if not _list:
        return None
        
    try:
        return _list[_index]
    except IndexError:
        return _list[0]


unit_ = []
for i, name in enumerate(unit_name_):
    
    unit = PHX.mechanicals.equipment.HVAC_Ventilator()
    
    # -- Basic Parameters for Ventilation Systems
    unit.SystemType = 1
    unit.TypeDevice = 1
    unit.UsedFor_Ventilation = True
    
    # -- Custom Attributes
    unit.Name = name or 'Unnamed Vent. Unit'
    unit.PH_Parameters.HeatRecoveryEfficiency = validate_efficiency(default_list_item(heat_recovery_eff_, i)) or unit.PH_Parameters.HeatRecoveryEfficiency
    unit.PH_Parameters.HumidityRecoveryEfficiency = validate_efficiency(default_list_item(moisture_recovery_eff_, i)) or unit.PH_Parameters.HumidityRecoveryEfficiency
    
    unit.PH_Parameters.ElectricEfficiency = default_list_item(electrical_eff_, i) or unit.PH_Parameters.ElectricEfficiency
    unit.PH_Parameters.TemperatureBelowDefrostUsed = default_list_item(frost_temp_, i) or unit.PH_Parameters.TemperatureBelowDefrostUsed
    unit.PH_Parameters.InConditionedSpace = default_list_item(install_location_, i) or unit.PH_Parameters.InConditionedSpace
    
    unit_.append(unit)
    
    PyPH_Rhino.gh_utils.object_preview(unit)