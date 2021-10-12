# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions for building PHX Mechanicals from Honeybee Rooms"""

from PHX.mechanicals.systems import MechanicalSystem
import PHX.mechanicals.equipment

from honeybee.room import Room


def PHX_Mech_Ventilation_from_HB_room(_hb_room: Room, _default: bool = False) -> MechanicalSystem:
    """Will return the user_data Mechanical Ventilation system, if any.
        If no user_data, will return default Ventiation System.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee room to use as the source.
        * _default (bool): default=False. If True, will return a default Ventilation System if no
            user_data is found. If False, will return None is no user_data is found.

    Returns:
    --------
        * (PHX.mechanicals.systems.MechanicalSystem | None): The PHX MechanicalSystem (Ventilation)
    """

    ud_mech_system_dict = (_hb_room.user_data or {}).get("phx", {}).get("mech_system_ventilation", None)
    if ud_mech_system_dict:
        # 1) -- Rebuild the MechSystem from the user-input
        return MechanicalSystem.from_dict(ud_mech_system_dict)
    elif _default:
        # 2) -- OK, no detailed User Input, Return the default ventilation, with default ventilator

        ventilation_sys = MechanicalSystem.default_ventilation()
        ventilator = PHX.mechanicals.equipment.HVAC_Ventilator.default()
        ventilation_sys.equipment_set.add_new_device_to_equipment_set(ventilator)

        return ventilation_sys
    else:
        return None


def PHX_Mech_HotWater_from_HB_room(_hb_room: Room, _default: bool = False) -> MechanicalSystem:
    """Will return the user_data Mechanical DHW system, if any.
        If no user_data, will return default DHW System.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee room to use as the source.
        * _default (bool): default=False. If True, will return a default HW System if no
            user_data is found. If False, will return None is no user_data is found.

    Returns:
    --------
        * (PHX.mechanicals.systems.MechanicalSystem | None): The PHX MechanicalSystem (DHW)
    """

    ud_mech_system_dict = (_hb_room.user_data or {}).get("phx", {}).get("mech_system_dhw", None)
    if ud_mech_system_dict:
        # 1) -- Rebuild the MechSystem from the user-input
        return MechanicalSystem.from_dict(ud_mech_system_dict)
    elif _default:
        # 2) -- OK, no detailed User Input, Return the default DHW System with tank

        dhw_sys = MechanicalSystem.default_hot_water()
        elec_heater = PHX.mechanicals.equipment.HW_Heater_Direct_Elec.default()
        dhw_sys.equipment_set.add_new_device_to_equipment_set(elec_heater)

        return dhw_sys
    else:
        return None
