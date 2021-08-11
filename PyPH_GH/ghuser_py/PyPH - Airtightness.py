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
Will calculate the PHPP Envelope Airtightness using the PHPP Rooms as the reference volume.
Connect the ouputs from this component to a Honeybee 'setEPZoneLoads' and then set the
Infiltration Schedule to 'CONSTANT'. Use a Honeybee 'Constant Schedule' with a value of
1 and a _schedTypeLimit of 'FRACTIONAL', then connect that to an HB 'setEPZoneSchdeules' component.
-
Note: The results shown here will be a fair bit different than the Honeybee 'ACH2m3/s-m2 Calculator'
standard component because for PH Cert we are supposed to use the Net Internal Volume (v50)
NOT the gross volume. E+ / HB use the gross volume and so given the same ACH, they will
arrive at different infiltration flow rates (flow = ACH * Volume). For PH work, use this component.
-
EM August 11, 2021
    Args:
        _n50: (ACH) The target ACH leakage rate
        _q50: (m3/hr-m2-surface) The target leakage rate per m2 of exposed surface area
        _pressure: (Pascal) Blower Door pressure for the airtightness measurement. Default is 50Pa
        _HBZones: Honeybee Zones to apply this leakage rate to. Note, this should 
            be the set of all the zones which were tested together as part of a
            Blower Door test. IE: if the blower door test included Zones A, B,
            and C then all three zones should be passed in here together. Use
            'Merge' to combine zones if need be.
    Returns:
        HB_rooms_: The Honeybee Room(s) with their Infiltration values modified.
"""

from honeybee_energy.load.infiltration import Infiltration
import LBT_Utils
import PyPH_Rhino.airtightness

# --- 
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Airtightness"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='AUG 11, 2021')

if DEV:
    reload(PyPH_Rhino.airtightness)
    reload(LBT_Utils)

# ---
HB_rooms_ = []
for room in _HB_rooms:
    if not room: continue
    
    # Calc the Zone's Infiltration Airflow based on the PHX Space's Volume
    # --------------------------------------------------------------------------
    room_infil_airflow = PyPH_Rhino.airtightness.calc_hb_room_infiltration_rate(
                                                                        room,
                                                                        _n50,
                                                                        _q50, 
                                                                        _pressure, 
                                                                        _preview=True)
    standard_flow_rate = PyPH_Rhino.airtightness.calc_standard_flow_rate(room_infil_airflow,
                                                                        _pressure)
    
    
    # --------------------------------------------------------------------------
    # Calc the Zone's Infiltration Rate in m3/hr-2 of floor area (zone gross)
    infilt_per_floor_area = standard_flow_rate /  room.floor_area  #m3/hr ---> m3/hr-m2-floor
    infilt_per_exterior_area = standard_flow_rate /  room.exposed_area  #m3/hr ---> m3/hr-m2-facade
    
    
    # --------------------------------------------------------------------------
    # Set the Load and Schedule for the HB-Room
    new_hb_room = room.duplicate()
    
    infilt_load = LBT_Utils.hb_loads.dup_load(new_hb_room, 'infiltration', Infiltration)
    infilt_load.flow_per_exterior_area = infilt_per_exterior_area
    LBT_Utils.hb_loads.assign_load(new_hb_room, infilt_load, 'infiltration')
    
    infiltration_sch_ = LBT_Utils.create_hb_constant_schedule( 'Infilt_Const_Sched' )
    infilt_sched = LBT_Utils.hb_loads.dup_load(new_hb_room, 'infiltration', 'infiltration_sch_')
    infilt_sched.schedule = infiltration_sch_
    LBT_Utils.hb_loads.assign_load(new_hb_room, infilt_sched, 'infiltration')
    
    HB_rooms_.append(new_hb_room)