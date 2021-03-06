import PHX.programs.ventilation
import PHX.programs.occupancy
import PHX.programs.lighting
import PHX.programs.electric_equipment
import PHX.programs.schedules
import PHX.programs.loads
import LBT_Utils.program
import LBT_Utils.hb_schedules

import honeybee.room


def _PHX_Vent_UtilRates_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.programs.schedules.Vent_UtilRates:
    """Return a new PHX Vent_UtilRates object with values set based on Honeybee Room.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room)

    Returns:
    --------
        * (PHX.programs.schedules.Vent_UtilRates)
    """
    # -- Generate the Data
    four_part_sched_values = LBT_Utils.program.calc_four_part_vent_sched_values_from_hb_room(_hb_room, _use_dcv=True)

    # -- Build the new Vent_UtilRates and set all the attributes
    new_util_rates = PHX.programs.schedules.Vent_UtilRates()

    daily_use_hours = 0.0

    values_high = four_part_sched_values.get(0, {})
    new_util_rates.maximum.daily_op_sched = values_high.get("frequency", 0) * 24
    new_util_rates.maximum.frac_of_design_airflow = values_high.get("average_value", 0)
    daily_use_hours += new_util_rates.maximum.daily_op_sched

    values_standard = four_part_sched_values.get(1, {})
    new_util_rates.standard.daily_op_sched = values_standard.get("frequency", 0) * 24
    new_util_rates.standard.frac_of_design_airflow = values_standard.get("average_value", 0)
    daily_use_hours += new_util_rates.standard.daily_op_sched

    values_basic = four_part_sched_values.get(2, {})
    new_util_rates.basic.daily_op_sched = values_basic.get("frequency", 0) * 24
    new_util_rates.basic.frac_of_design_airflow = values_basic.get("average_value", 0)
    daily_use_hours += new_util_rates.basic.daily_op_sched

    values_minimum = four_part_sched_values.get(3, {})
    new_util_rates.minimum.daily_op_sched = 24.0 - daily_use_hours  # Enforce max 24 hr
    new_util_rates.minimum.frac_of_design_airflow = values_minimum.get("average_value", 0)

    return new_util_rates


def create_PHX_RoomVentilation_from_hb_room(_hb_room: honeybee.room.Room) -> PHX.programs.ventilation.RoomVentilation:
    """
    Returns a PHX-Ventilation Program Object, with attributes based on an input Honeybee Ventilation Object

    Arguments:
    ---------
        * _hb_room (honeybee.room.Room): The Honeybee room to build the Ventilation object from.

    Returns:
    --------
        * (PHX.programs.ventilation.RoomVentilation):
    """

    phx_Ventilation = PHX.programs.ventilation.RoomVentilation()

    # -- Sort out the Names (Obj, Load, Schedule)
    phx_Ventilation.name = LBT_Utils.program.clean_HB_program_name(_hb_room.properties.energy.ventilation.display_name)
    phx_Ventilation.loads.name = LBT_Utils.program.clean_HB_program_name(
        _hb_room.properties.energy.ventilation.display_name
    )
    if _hb_room.properties.energy.ventilation.schedule is not None:
        phx_Ventilation.schedule.name = LBT_Utils.program.clean_HB_program_name(
            _hb_room.properties.energy.ventilation.schedule.display_name
        )
    else:
        phx_Ventilation.schedule.name = LBT_Utils.program.clean_HB_program_name(
            _hb_room.properties.energy.ventilation.display_name
        )

    phx_Ventilation.name = phx_Ventilation.name + "_vent"
    phx_Ventilation.loads.name = phx_Ventilation.name + "_vent_loads"
    phx_Ventilation.schedule.name = phx_Ventilation.schedule.name + "_vent_sched"

    # -- Sort out the Identifiers (Obj, Load, Schedule)
    phx_Ventilation.identifier = _hb_room.properties.energy.ventilation.identifier
    phx_Ventilation.loads.identifier = _hb_room.properties.energy.ventilation.identifier

    if _hb_room.properties.energy.ventilation.schedule is not None:
        phx_Ventilation.schedule.identifier = _hb_room.properties.energy.ventilation.schedule.identifier
    else:
        phx_Ventilation.schedule.identifier = _hb_room.properties.energy.ventilation.identifier

    # --------------------------------------------------------------------------
    # -- Convert the Ventilation Loads from HB to PH
    if getattr(_hb_room.properties.energy.ventilation, "user_data", None):
        # -- Try and get any user-determined inputs
        ud_loads = (_hb_room.properties.energy.ventilation.user_data or {}).get("phx", {}).get("loads", None)
        print("trying to use UD Vent. Loads (.user_data), but that isnt written yet....")

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
    # -- Convert the Ventilation Schedule from HB to PH
    if getattr(_hb_room.properties.energy.ventilation, "user_data", None):
        # -- Try and just use simplified user-input values

        print("trying to use the UD Vent Schedule (.user_data), but I haven't written this part yet")

        #
        #
        #
        # TODO
        #
        #
        #

    else:
        # -- Calc and Apply the PH-Style Schedule Values
        phx_Ventilation.schedule.operating_days = 7
        phx_Ventilation.schedule.operating_weeks = 52
        phx_Ventilation.schedule.utilization_rates = _PHX_Vent_UtilRates_from_HB_room(_hb_room)

    return phx_Ventilation


def create_PHX_RoomOccupancy_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.programs.occupancy.RoomOccupancy:
    """Returns a new PHX RoomOccupancy object with attributes based on the Honeybee Room.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee room to build the RoomOccupancy object from.

    Returns:
    --------
        * (PHX.programs.occupancy.RoomOccupancy): The new RoomOccupancy object, with attributes
            defined by the Honeybee Room's Occupancy Program.
    """

    phx_occ_program = PHX.programs.occupancy.RoomOccupancy()

    # --------------------------------------------------------------------------
    # -- Sort out the HB Loads, if any
    if _hb_room.properties.energy.people is None:
        # -- Build the default Occupancy, based on the Program name
        clean_name = LBT_Utils.program.clean_HB_program_name(_hb_room.properties.energy.program_type.display_name)
        no_occupancy_name = "{}_[no_HB_occ]".format(clean_name)
        phx_occ_program.name = no_occupancy_name
        phx_occ_program.loads.name = phx_occ_program.name
        phx_occ_program.schedule.name = phx_occ_program.name

        phx_occ_program.loads.people_per_area = 0
        phx_occ_program.schedule.annual_utilization_factor = 0

        return phx_occ_program

    phx_occ_program.name = LBT_Utils.program.clean_HB_program_name(_hb_room.properties.energy.people.display_name)
    phx_occ_program.loads.name = phx_occ_program.name
    phx_occ_program.loads.people_per_area = _hb_room.properties.energy.people.people_per_area

    # --------------------------------------------------------------------------
    # -- Sort out the HB Schedule, if any
    if _hb_room.properties.energy.people.occupancy_schedule is None:
        phx_occ_program.schedule.name = phx_occ_program.name
        phx_occ_program.schedule.annual_utilization_factor = 1.0
        return phx_occ_program

    hb_sched = _hb_room.properties.energy.people.occupancy_schedule
    phx_occ_program.schedule.name = hb_sched.display_name
    phx_occ_program.schedule.annual_utilization_factor = LBT_Utils.hb_schedules.calc_utilization_factor(hb_sched)

    # --------------------------------------------------------------------------
    # -- Override Schedule with UD custom from user_data, if it exists
    ud_sched_dict = (
        (_hb_room.properties.energy.people.occupancy_schedule.user_data or {}).get("phx", {}).get("schedule_occupancy")
    )
    if ud_sched_dict:
        phx_schedule = PHX.programs.schedules.Schedule_Occupancy.from_dict(ud_sched_dict)
        phx_occ_program.schedule = phx_schedule

    return phx_occ_program


def create_PHX_RoomLighting_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.programs.lighting.RoomLighting:
    """Returns a new PHX RoomLighting object with attributes based on the Honeybee Room.

    Arugments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee room to build the RoomLighting object from.

    Returns:
    --------
        * (PHX.programs.lighting.RoomLighting): The new RoomLighting object, with attributes
            defined by the Honeybee Room's Lighting Program.
    """

    phx_lighting_program = PHX.programs.lighting.RoomLighting()

    # --------------------------------------------------------------------------
    # -- Sort out the Loads, if any
    if _hb_room.properties.energy.lighting is None:
        clean_name = LBT_Utils.program.clean_HB_program_name(_hb_room.properties.energy.program_type.display_name)
        no_occupancy_name = "{}_[no_HB_lght]".format(clean_name)
        phx_lighting_program.name = no_occupancy_name
        phx_lighting_program.loads.name = phx_lighting_program.name
        phx_lighting_program.schedule.name = phx_lighting_program.name
        return phx_lighting_program

    phx_lighting_program.name = LBT_Utils.program.clean_HB_program_name(
        _hb_room.properties.energy.lighting.display_name
    )
    phx_lighting_program.loads.name = phx_lighting_program.name
    phx_lighting_program.loads.target_lux = 300  # default
    phx_lighting_program.loads.target_lux_height = 0.8  # meters. default
    phx_lighting_program.loads.watts_per_area = _hb_room.properties.energy.lighting.watts_per_area

    # --------------------------------------------------------------------------
    # -- Sort out the Schedule, if any
    if _hb_room.properties.energy.lighting.schedule is None:
        phx_lighting_program.schedule.name = phx_lighting_program.name
        phx_lighting_program.schedule.annual_utilization_factor = 1.0
        return phx_lighting_program

    hb_sched = _hb_room.properties.energy.lighting.schedule
    phx_lighting_program.schedule.name = hb_sched.display_name
    phx_lighting_program.schedule.annual_utilization_factor = LBT_Utils.hb_schedules.calc_utilization_factor(hb_sched)

    # --------------------------------------------------------------------------
    # -- Override Load with UD custom from user_data, if it exists
    ud_load_dict = (_hb_room.properties.energy.lighting.user_data or {}).get("phx", {}).get("load_lighting")
    ud_sched_dict = (
        (_hb_room.properties.energy.lighting.schedule.user_data or {}).get("phx", {}).get("schedule_lighting")
    )
    if ud_load_dict:
        phx_lighting_program.loads = PHX.programs.loads.Load_Lighting.from_dict(ud_load_dict)

    if ud_sched_dict:
        phx_lighting_program.schedule = PHX.programs.schedules.Schedule_Lighting.from_dict(ud_sched_dict)

    return phx_lighting_program


def create_PHX_RoomElectricEquipment_from_HB_room(
    _hb_room: honeybee.room.Room,
) -> PHX.programs.electric_equipment.RoomElectricEquipment:

    phx_elec_equip_program = PHX.programs.electric_equipment.RoomElectricEquipment()

    # --------------------------------------------------------------------------
    # -- Sort out the Loads, if any
    if _hb_room.properties.energy.electric_equipment is None:
        clean_name = LBT_Utils.program.clean_HB_program_name(_hb_room.properties.energy.program_type.display_name)
        no_occupancy_name = "{}_[no_HB_elec_equip]".format(clean_name)
        phx_elec_equip_program.name = no_occupancy_name
        phx_elec_equip_program.loads.name = phx_elec_equip_program.name
        phx_elec_equip_program.schedule.name = phx_elec_equip_program.name
        return phx_elec_equip_program

    phx_elec_equip_program.name = LBT_Utils.program.clean_HB_program_name(
        _hb_room.properties.energy.electric_equipment.display_name
    )
    phx_elec_equip_program.loads.name = phx_elec_equip_program.name
    phx_elec_equip_program.loads.watts_per_area = _hb_room.properties.energy.electric_equipment.watts_per_area

    # --------------------------------------------------------------------------
    # -- Sort out the Schedule, if any
    if _hb_room.properties.energy.electric_equipment.schedule is None:
        phx_elec_equip_program.schedule.name = phx_elec_equip_program.name
        phx_elec_equip_program.schedule.annual_utilization_factor = 1.0
        return phx_elec_equip_program

    hb_sched = _hb_room.properties.energy.electric_equipment.schedule
    phx_elec_equip_program.schedule.name = hb_sched.display_name
    phx_elec_equip_program.schedule.annual_utilization_factor = LBT_Utils.hb_schedules.calc_utilization_factor(
        hb_sched
    )

    # --------------------------------------------------------------------------
    # -- Override Load with UD custom from user_data, if it exists
    ud_load_dict = (
        (_hb_room.properties.energy.electric_equipment.user_data or {}).get("phx", {}).get("load_elec_equipment")
    )
    ud_sched_dict = (
        (_hb_room.properties.energy.electric_equipment.schedule.user_data or {})
        .get("phx", {})
        .get("schedule_elec_equipment")
    )
    if ud_load_dict:
        phx_elec_equip_program.loads = PHX.programs.loads.Load_ElecEquip.from_dict(ud_load_dict)

    if ud_sched_dict:
        phx_elec_equip_program.schedule = PHX.programs.schedules.Schedule_ElecEquip.from_dict(ud_sched_dict)

    return phx_elec_equip_program
