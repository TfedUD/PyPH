import honeybee_energy.load.lighting
import LBT_Utils.program
import LBT_Utils.hb_schedules
import PHX.programs.lighting


def phx_lighting_from_hb(_hb_lighting):
    # type: (honeybee_energy.load.lighting.Lighting) -> PHX.programs.lighting.RoomLighting

    lighting = PHX.programs.lighting.RoomLighting()

    if _hb_lighting:
        lighting.name = LBT_Utils.program.clean_HB_program_name(_hb_lighting.display_name)
        lighting.loads.watts_per_area = _hb_lighting.watts_per_area

        # Utilization Rates
        annual_util = LBT_Utils.hb_schedules.calc_utilization_factor(_hb_lighting.schedule)
        lighting.schedule.annual_utilization_factor = annual_util

    return lighting
