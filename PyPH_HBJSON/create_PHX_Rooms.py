# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions used to build PHX Rooms from Honeybee Rooms"""

import PHX.bldg_segment
import honeybee.room
import PyPH_HBJSON.create_PHX_Ventilation
import PHX.mechanicals.systems
import PHX.mechanicals.equipment


def create_PHX_Room_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.bldg_segment.Room:
    room = PHX.bldg_segment.Room()
    room.name = _hb_room.display_name
    room.volume_gross = _hb_room.volume

    # -- Set the Ventilation Program
    room.ventilation = PyPH_HBJSON.create_PHX_Ventilation.PHX_ventilation_from_hb_room(_hb_room)

    return room


def create_PHX_Mechanicals_from_HB_room(_hb_room):
    ud_mech_system_dict = (_hb_room.user_data or {}).get("phx", {}).get("mechanicals", {})

    if ud_mech_system_dict:
        # -- Rebuild the MechSystem from the user-input
        mech = PHX.mechanicals.systems.Mechanicals()
        mech.add_system(PHX.mechanicals.systems.MechanicalSystem.from_dict(ud_mech_system_dict))
    else:
        # -- No detailed User Input, add the default system with a default ventilator
        mech = PHX.mechanicals.systems.Mechanicals()

        # -- Build the default ventilation, and ventilator. Add to the system
        ventilator = PHX.mechanicals.equipment.HVAC_Ventilator.default()
        ventilation_sys = PHX.mechanicals.systems.MechanicalSystem.default_ventilation()
        ventilation_sys.equipment_set.add_new_device_to_equipment_set(ventilator)

        # -- Add the Vent sytstem to the Mechanicals Object
        mech.add_system(ventilation_sys)

    return mech
