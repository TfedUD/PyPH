# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions for building PHX Mechanicals from Honeybee Rooms"""

import PHX.mechanicals.systems
import PHX.mechanicals.equipment

import honeybee.room


def create_PHX_Mechanicals_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.mechanicals.systems.Mechanicals:
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


def create_system_from_hb_room(_hb_room: honeybee.room.Room) -> PHX.mechanicals.systems.MechanicalSystem:
    # -- Get the Default Ventilator
    ventilator = PHX.mechanicals.equipment.HVAC_Ventilator.default()
    ventilator.name = "Room Ventilator"

    # -- Create the Default Ventilation System, Add the default Ventilator
    vent_sys = PHX.mechanicals.systems.MechanicalSystem.default_ventilation()
    vent_sys.equipment.add_new_device_to_equipment_set(ventilator)

    # -- Get and assign any user-defined Ventilator / System info found at the Room level
    #
    #
    # TODO
    #
    #

    return vent_sys
