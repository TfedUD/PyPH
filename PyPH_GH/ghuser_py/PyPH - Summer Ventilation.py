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
Use this component to add summmer ventilation to Honeybee rooms. This controls 
the inputs on the PHPP 'SummVent' worksheet. Use this to input the total daytime 
and nighttime ACH from any 'additional' ventilation beyond the basic HRV/ERV. 
This could be from operable windows, additional fans or any other method used to 
increase airflow during the summer months.

NOTE: For Phius, as per Phius 2021 PH Building Standard Certification Guidebook v3.02, Jult 2021:
" If a cooling system is planned, no natural ventilation may be 
included in the model. An entry of ‘0’ is required for PHIUS+ 2018 or Phius 2021 certification."
-
EM October 19, 2021
    Args:
        mech_ach_: (float) The summer-period average background ventilation ACH rate of the Ventilator 
            (HRV/ERV). In most cases, this will be the same value as the winter-perido, although
            in some cases the designer may wish to run the ventilator at a higher rate in summer. 
            NOTE: For Phius projects, in most cases simply set this input to "Phius", which then
            will autocalculate the summer ventilation flow-rate.
        mech_control_: (str)
        
        use_default_: (boolean) Default=False. Set True to use 'default' values
            for all summer-vent. This is recommended.
        
        window_day_ach_: The Air-Changes-per-Hour (ACH) from windows during the daytime.
            Note, this value gets applied to EACH HB-Room you pass in. In the 
            PHPP, the SummVent worksheet will be the Total of all the HB-Room ACH values.
        
        window_night_ach_: The Air-Changes-per-Hour (ACH) from windows during the nighttime. 
            Note, this value gets applied to EACH HB-Room you pass in. In the PHPP, 
            the SummVent worksheet will be the Total of all the HB-Room ach values.
            
        addnl_mech_ach_: (float)
        addnl_mech_fan_pwr_: (float) 
        addnl_mech_control_: (str)
            
        exhaust_ach_: (float)
        exhaust_fan_pwr_: (str)
        
        _HB_rooms: The Honeybee Rooms, with PHX-Spaces, to apply the new ventilation to

    Returns:
        HB_rooms_: The Honeybee Room(s) with their Spaces and Ventilation modified.
"""

import LBT_Utils
import PHX
import PHX.summer_ventilation
import PyPH_Rhino.gh_utils

# --- 
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Summer Ventilation"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_19_2021')

if DEV:
    reload(PHX.summer_ventilation)
    reload(LBT_Utils)
    reload(LBT_Utils.program)
    reload(PHX.serialization.to_dict)
    reload(PHX)
    reload(PyPH_Rhino.gh_utils)

def handle_mech_ach(_input):
    """Handle the input types for avg summer-period mech vent ACH
    
    > if no input, return 0.0 ACH
    > if a number input, return as a number
    > if 'PHIUS' input, return 'None'
    """
    
    if not _input:
        return 0.0
    
    try:
        return float(_input)
    except ValueError:
        if 'PHIUS' in str(_input).upper():
            # None = bank in WUFI, so it autocalculates.
            return None

HB_rooms_ = []
for hb_room in _HB_rooms:
    #-------------------------------------------------------------------------------
    # Build the SummerVent Object
    summ_vent_obj = PHX.summer_ventilation.SummerVent()
    
    if use_defaults_:
        avg_annual_vent_ach = LBT_Utils.program.calc_HB_room_avg_ventilation_ach(hb_room)
        summ_vent_obj.day_window_ach = avg_annual_vent_ach * 0.5
        summ_vent_obj.night_window_ach = avg_annual_vent_ach * 0.5
    
    #-- Basic HRV Ventilation
    if mech_ach_ is not None: summ_vent_obj.avg_mech_ach = handle_mech_ach(mech_ach_)
    if mech_control_ is not None: summ_vent_obj.avg_mech_control_mode = mech_control_
    
    #-- Window Ventilation
    if window_day_ach_ is not None: summ_vent_obj.day_window_ach = window_day_ach_
    if window_night_ach_ is not None: summ_vent_obj.night_window_ach = window_night_ach_
    
    #-- Additional Ventilation
    if addnl_mech_ach_ is not None: summ_vent_obj.additional_mech_ach = addnl_mech_ach_
    if addnl_mech_fan_pwr_ is not None: summ_vent_obj.additional_mech_spec_power = addnl_mech_fan_pwr_
    if addnl_mech_control_ is not None: summ_vent_obj.additional_mech_control_mode = addnl_mech_control_
    if exhaust_ach_ is not None: summ_vent_obj.exhaust_ach = exhaust_ach_
    if exhaust_fan_pwr_ is not None: summ_vent_obj.exhaust_spec_power = exhaust_fan_pwr_
    
    d = summ_vent_obj.to_dict()
    
    
    #-------------------------------------------------------------------------------
    # Add the Summ-Vent objects onto the Honeybee Rooms
    
    new_hb_room = hb_room.duplicate()
    new_hb_room = LBT_Utils.user_data.add_to_HB_Obj_user_data(new_hb_room,
                                        d, 'summ_vent', _write_mode='overwrite')
    
    HB_rooms_.append( new_hb_room )
    
    PyPH_Rhino.gh_utils.object_preview(summ_vent_obj)