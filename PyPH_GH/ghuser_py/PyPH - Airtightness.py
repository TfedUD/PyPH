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
EM August 20, 2021
    Args:
        _n50: (ACH) The target ACH leakage rate.
            
            For PHI Certification (@50Pa):
                * New Construction: < 0.6 ACH
                * Retrofit: < 1.0 ACH
                * Low-Energy Building < 1.0 ACH
        _q50: (m3/s per m2-surface) The target leakage rate per m2 of exposed surface area.
            Gross envelope is measured at the exterior of the thermal boundary, the 
            same as for the energy model, and includes surfaces in contact with the ground.
            
            For PHIUS 2021 Certification (@5OPa):
                * Buildings 5-stories or above and non-combustible: _____ m3/s-m2 [0.080 CFM/ft2]
                * All others: < ______ m3/s-m2 [0.060 CFM/ft2]
            
            For PHI Certification (@50Pa):
                * Recommendation < 0.00017 m3/s-m2 [ _____ CFM/ft2]
        
        _blower_pressure: (Pascal) Blower Door pressure for the airtightness measurement. Default is 50Pa
        _HBZones: Honeybee Zones to apply this leakage rate to. Note, this should 
            be the set of all the zones which were tested together as part of a
            Blower Door test. IE: if the blower door test included Zones A, B,
            and C then all three zones should be passed in here together. Use
            'Merge' to combine zones if need be.
    Returns:
        HB_rooms_: The Honeybee Room(s) with their Infiltration values modified.
"""

from honeybee_energy.properties.room import RoomEnergyProperties
from honeybee_energy.load.infiltration import Infiltration
import LBT_Utils
import LBT_Utils.boundary_conditions
import PyPH_Rhino.airtightness

# --- 
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Airtightness"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='AUG 20, 2021')

if DEV:
    reload(PyPH_Rhino.airtightness)
    reload(LBT_Utils)
    reload(LBT_Utils.boundary_conditions)

# ---
infiltration_sch_ = LBT_Utils.create_hb_constant_schedule( 'Infilt_Const_Sched' )

HB_rooms_ = []
for room in _HB_rooms:
    if not room: continue
    
    print("{} HB-Room: {}{}".format("- " * 15, room.display_name, "- " * 15))
    
    room_exposed_area = LBT_Utils.boundary_conditions.hb_room_PHX_exposed_area(room)
    if room_exposed_area:
        
        # Calc the Zone's Infiltration Airflow based on the PHX Space's Volume
        # --------------------------------------------------------------------------
        room_infil_m3s_at_test_pressure = PyPH_Rhino.airtightness.calc_hb_room_infiltration_m3s(
                                                    room, _n50, _q50, 
                                                    _blower_pressure, _preview=True)
        
        # --------------------------------------------------------------------------
        # -- Covert down to 4Pa which is what Honeybee uses for inputs
        # -- Compute coeffiecient and airflow@ 4Pa
        bldg_pressure = 4 #Pa
        
        #-- Get the infiltration airflow at test pressure
        room_infil_m3sm2_at_test_pressure = room_infil_m3s_at_test_pressure / room_exposed_area
        
        #-- Convert to resting pressure
        C_qa = RoomEnergyProperties.solve_norm_area_flow_coefficient(
            room_infil_m3sm2_at_test_pressure, air_density=1, delta_pressure=_blower_pressure)
        room_infil_m3sm2_at_rest_pressure = C_qa * (bldg_pressure ** 0.65)
        
        # -- More preview.... so many values!!
        print '  > HB-Room: Specific infiltration rate at normal pressure:'
        print '  >     {:.04f} m3/h-m2 ({:.06f} m3/s-m2) @4Pa'.format(room_infil_m3sm2_at_rest_pressure*3600, room_infil_m3sm2_at_rest_pressure)
        print '  > HB-Room: Absolute infiltration rate at normal pressure:'
        print '  >     {:.01f} m3/h @4Pa ({:.06f} m3/s)'.format(
            room_infil_m3sm2_at_rest_pressure*3600*room_exposed_area,
            room_infil_m3sm2_at_rest_pressure*room_exposed_area)
    else:
        print("NOTE: No Exposed Area. No Infiltration.")
        room_infil_m3sm2_at_rest_pressure = 0
    
    # --------------------------------------------------------------------------
    # Set the Load and Schedule for the HB-Room
    new_hb_room = room.duplicate()
    
    infilt_load = LBT_Utils.hb_loads.dup_load(new_hb_room, 'infiltration', Infiltration)
    infilt_load.flow_per_exterior_area = room_infil_m3sm2_at_rest_pressure
    LBT_Utils.hb_loads.assign_load(new_hb_room, infilt_load, 'infiltration')
    
    infilt_sched = LBT_Utils.hb_loads.dup_load(new_hb_room, 'infiltration', 'infiltration_sch_')
    infilt_sched.schedule = infiltration_sch_
    LBT_Utils.hb_loads.assign_load(new_hb_room, infilt_sched, 'infiltration')
    
    HB_rooms_.append(new_hb_room)