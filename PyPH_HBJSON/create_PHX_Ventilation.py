import PHX.programs.ventilation
import PHX.programs.loads
import PHX.programs.schedules
import PHX.hvac_components
import PHX.bldg_segment
import LBT_Utils.program

import honeybee.room


def PHX_ventilation_from_hb_room(_hb_room: honeybee.room.Room):
    """
    Returns a PHX-Ventilation Object, with attributes based on an input Honeybee Ventilation Object

    Arguments:
    ---------
        * _hb_room (honeybee.room.Room): The Honeybee room to build the Ventilation object from.
    """

    phx_Ventilation = PHX.programs.ventilation.RoomVentilation()
    phx_Ventilation.name = _hb_room.properties.energy.ventilation.display_name
    phx_Ventilation.identifier = _hb_room.properties.energy.ventilation.identifier
    phx_Ventilation.loads.identifier = _hb_room.properties.energy.ventilation.identifier
    phx_Ventilation.schedule.identifier = _hb_room.properties.energy.ventilation.identifier

    # --------------------------------------------------------------------------
    # -- Convert the Loads
    if getattr(_hb_room.properties.energy.ventilation, "user_data", None):
        # -- Try and get any user-determined inputs
        ud_loads = (_hb_room.properties.energy.ventilation.user_data or {}).get("phx", {}).get("loads", None)
        print("trying to use UD Vent. Loads, but that isnt written yet....")

        #
        #
        #
        # TODO
        #
        #
        #
    else:
        # -- If no UD inputs, convert the normal HB Loads
        hb_room_vent_flow_m3h = LBT_Utils.program.calc_HB_Room_total_ventilation_m3sec(_hb_room) * 3600
        phx_Ventilation.loads.name = phx_Ventilation.name
        phx_Ventilation.loads.supply = hb_room_vent_flow_m3h
        phx_Ventilation.loads.extract = hb_room_vent_flow_m3h
        phx_Ventilation.loads.transfer = hb_room_vent_flow_m3h

    # --------------------------------------------------------------------------
    # -- Convert the Schedule
    if getattr(_hb_room.properties.energy.ventilation, "user_data", None):
        # -- Try and just use simplified user-input values
        print("trying to use the UD Vent Schedule, but I haven't written this part yet")

        #
        #
        #
        # TODO
        #
        #
        #

    else:
        # -- Calc and Apply the PH-Style
        new_util_rates = PHX.programs.schedules.Vent_UtilRates()
        four_part_sched_values = LBT_Utils.program.calc_four_part_vent_sched_values_from_hb_room(_hb_room)

        values_high = four_part_sched_values.get(0, {})
        new_util_rates.maximum.daily_op_sched = values_high.get("frequency", 0) * 24
        new_util_rates.maximum.frac_of_design_airflow = values_high.get("value_frac_of_max", 0)

        values_standard = four_part_sched_values.get(1, {})
        new_util_rates.standard.daily_op_sched = values_standard.get("frequency", 0) * 24
        new_util_rates.standard.frac_of_design_airflow = values_standard.get("value_frac_of_max", 0)

        values_basic = four_part_sched_values.get(2, {})
        new_util_rates.basic.daily_op_sched = values_basic.get("frequency", 0) * 24
        new_util_rates.basic.frac_of_design_airflow = values_basic.get("value_frac_of_max", 0)

        values_minimum = four_part_sched_values.get(3, {})
        new_util_rates.minimum.daily_op_sched = values_minimum.get("frequency", 0) * 24
        new_util_rates.minimum.frac_of_design_airflow = values_minimum.get("value_frac_of_max", 0)

        phx_Ventilation.schedule.name = LBT_Utils.program.clean_HB_program_name(phx_Ventilation.name)
        phx_Ventilation.schedule.operating_days = 7
        phx_Ventilation.schedule.operating_weeks = 52
        phx_Ventilation.schedule.utilization_rates = new_util_rates

    return phx_Ventilation


def get_ventilator_from_hb_room(_hb_room: honeybee.room.Room):
    ventilator = PHX.hvac_components.HVAC_Ventilator()
    ventilator.Name = "Room Ventilator"
    ventilator.UsedFor_Ventilation = True

    return ventilator
