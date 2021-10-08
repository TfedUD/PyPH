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
Use this component to load PHIUS Programs for people, lighting and electrical equipment
from the PHIUS Standards dictioanry. These prrograms are a combination of data drawn from:
    - PHIUS_Multi-Family_Calculator- 021.03.23.xls
    - PHIUS Guidebook, Table N-10, v3.02 | July 2021
    - Honeybee ASHRAE 90.1 2019 | IECC 2021
    
    To search for a program type based on the name found in the PHIUS Guidebook Table N-10,
    enter the name in the _description input.
    
    If a matching program is found, these can be combiend with a base Honeybee program using 
    the Honeybee "Program Type" component.
-
EM October 08, 2021
    Args:
        _name: (str) A text name to search the PHIUS dictionary for.
        _description: (str) A text description  / keyword to seach the PHIUS dictionary
            'description' field for.
    Returns:
        people_: A Honeybee People program, if a matching PHIUS program is found.
        lighting_: A Honeybee Lighting program, if a matching PHIUS program is found.
        elec_equipment_ :A Honeybee Electrical Equipment program, if a matching PHIUS program is found.
"""

from honeybee_energy.load.people import People
from honeybee_energy.load.lighting import Lighting
from honeybee_energy.load.equipment import ElectricEquipment, GasEquipment

import LBT_Utils
import PHX.programs.schedules
import PHX.programs.loads
import PHX.standards.PHIUS_programs

# --- 
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Get PHIUS Program"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_08_2021')

if DEV:
    reload( LBT_Utils)
    reload( PHX.programs.schedules)
    reload( PHX.programs.loads)
    reload(PHX.standards.PHIUS_programs)

# -- Preview
print 'Available PHIUS Program Names:'
for _ in PHX.standards.PHIUS_programs.PHIUS_library.keys():
    print "- {}".format(_)


# -- Find and Load the PHIUS Program Dict by Name
program_dicts = []
for search_name in _name:
    for k, v in PHX.standards.PHIUS_programs.PHIUS_library.items():
        if search_name.upper() in k.upper():
            program_dicts.append(v)
            break
    else:
        program_dicts.append(None)


# -- Find and Load the PHIUS Program Dict by Description
for search_name in _description:
    for k, v in PHX.standards.PHIUS_programs.PHIUS_library.items():
        if search_name.upper() in v.get('description').upper():
            program_dicts.append(v)
            break
    else:
        program_dicts.append(None)


# -- Convert the Dict values to actual PHX / HB Programs
people_ = []
lighting_ = []
elec_equipment_ = []
for program_dict in program_dicts:
    # -- Set as None so that output list len matches input list length
    people = None
    lighting = None
    elec_equip = None
    
    if program_dict:
        # ----------------------------------------------------------------------
        # -- PEOPLE ---
        people_schd_dict = program_dict.get('people', {}).get('schedule')
        people_load_dict = program_dict.get('people', {}).get('loads')
        if people_schd_dict and people_load_dict:
            # -- Schedule
            people_sched = PHX.programs.schedules.Schedule_Occupancy.from_dict(people_schd_dict)
            HB_occupancy_sched_ = LBT_Utils.hb_schedules.create_hb_constant_schedule(people_sched.name,
                    _value=people_sched.annual_utilization_factor)
                    
            HB_occupancy_sched_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(HB_occupancy_sched_, 
                    people_sched.to_dict(), 'schedule_occupancy', _write_mode='overwrite')
            
            # --Load
            people_load = PHX.programs.loads.Load_Occupancy.from_dict(people_load_dict)
            people = People(people_load.name, people_load.people_per_area, HB_occupancy_sched_)
            people = LBT_Utils.user_data.add_to_HB_Obj_user_data(people, 
                    people_load.to_dict(), 'load_occupancy', _write_mode='overwrite')
        
        # ----------------------------------------------------------------------
        # -- LIGHTING ---
        lighting_schd_dict = program_dict.get('lighting', {}).get('schedule')
        lighting_load_dict = program_dict.get('lighting', {}).get('loads')
        if lighting_schd_dict and lighting_load_dict:
            # -- Schedule
            lighting_sched = PHX.programs.schedules.Schedule_Lighting.from_dict(lighting_schd_dict)
            HB_lighting_sched_ = LBT_Utils.hb_schedules.create_hb_constant_schedule(lighting_sched.name,
                    _value=lighting_sched.annual_utilization_factor)
                    
            HB_lighting_sched_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(HB_lighting_sched_, 
                    lighting_sched.to_dict(), 'schedule_lighting', _write_mode='overwrite')
            
            # --Load
            lighting_load = PHX.programs.loads.Load_Lighting.from_dict(lighting_load_dict)
            lighting = Lighting(lighting_load.name, lighting_load.watts_per_area, HB_lighting_sched_)
            lighting = LBT_Utils.user_data.add_to_HB_Obj_user_data(lighting, 
                    lighting_load.to_dict(), 'load_lighting', _write_mode='overwrite')
        
        
        # ----------------------------------------------------------------------
        # -- ELEC. EQUIPMENT ---
        elec_equipment_schd_dict = program_dict.get('elec_equipment', {}).get('schedule')
        elec_equipment_load_dict = program_dict.get('elec_equipment', {}).get('loads')
        if elec_equipment_schd_dict and elec_equipment_load_dict:
            # -- Schedule
            elec_equip_sched = PHX.programs.schedules.Schedule_ElecEquip.from_dict(elec_equipment_schd_dict)
            HB_elec_equip_sched_ = LBT_Utils.hb_schedules.create_hb_constant_schedule(elec_equip_sched.name,
                    _value=elec_equip_sched.annual_utilization_factor)
            
            HB_elec_equip_sched_ = LBT_Utils.user_data.add_to_HB_Obj_user_data(HB_elec_equip_sched_, 
                    elec_equip_sched.to_dict(), 'schedule_elec_equipment', _write_mode='overwrite')
            
            # --Load
            elec_equip_load = PHX.programs.loads.Load_Lighting.from_dict(elec_equipment_load_dict)
            elec_equip = ElectricEquipment(elec_equip_load.name, elec_equip_load.watts_per_area, HB_elec_equip_sched_)
            elec_equip = LBT_Utils.user_data.add_to_HB_Obj_user_data(elec_equip, 
                    elec_equip_load.to_dict(), 'load_elec_equipment', _write_mode='overwrite')
    
    people_.append(people)
    lighting_.append(lighting)
    elec_equipment_.append(elec_equip)

