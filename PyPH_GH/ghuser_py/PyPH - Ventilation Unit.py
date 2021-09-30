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
EM August 25, 2021
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

import PHX.hvac
import PHX.hvac_components

# --
import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.name = "PyPH - Ventilation Unit"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="AUG 25, 2021")

if DEV:
    reload(PHX.hvac)
    reload(PHX.hvac_components)


def validate_efficiency(_in):
    if not _in:
        return None

    if float(_in) > 1:
        return float(_in) / 100
    else:
        return float(_in)


unit_ = PHX.hvac_components.Ventilator()

# -- Basic Parameters for Ventilation Systems
unit_.system_type = 1
unit_.device_type = 1
unit_.UsedFor_Ventilation = True

# -- Custom Attributes
unit_.name = unit_name_ or "Unnamed Vent. Unit"
unit_.PH_Parameters.HeatRecoveryEfficiency = (
    validate_efficiency(heat_recovery_eff_) or unit_.PH_Parameters.HeatRecoveryEfficiency
)
unit_.PH_Parameters.HumidityRecoveryEfficiency = (
    validate_efficiency(moisture_recovery_eff_) or unit_.PH_Parameters.HumidityRecoveryEfficiency
)

unit_.PH_Parameters.ElectricEfficiency = electrical_eff_ or unit_.PH_Parameters.ElectricEfficiency
unit_.PH_Parameters.TemperatureBelowDefrostUsed = frost_temp_ or unit_.PH_Parameters.TemperatureBelowDefrostUsed
unit_.PH_Parameters.InConditionedSpace = install_location_ or unit_.PH_Parameters.InConditionedSpace
