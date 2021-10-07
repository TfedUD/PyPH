# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to convert data from PHX objects into WUFI-specific format.

These functions get called before the object is passed to the XML-Schema
and will construct all the required 'temp' objects needed in order to 
re-organize the PHX objects into WUFI-compatible shape.

Each function here should have a name which matches the PHX class name, 
preceeded by an undrscore: "_" ie: Room --> "_Room".
"""

from dataclasses import dataclass, field
from typing import Union

import PHX.spaces
import PHX.programs.schedules
import PHX.programs.lighting
import PHX.programs.occupancy
import PHX.programs.ventilation
import PHX.programs.electric_equipment
import PHX.bldg_segment
import PHX.mechanicals.systems
from PyPH_WUFI.utilization_patterns import UtilizationPattern_NonRes, UtilizationPattern_Vent

TOL = 2  # Value tolerance for rounding. ie; 9.84318191919 -> 9.84


@dataclass
class temp_RoomVentilation:
    ventilator_id: int = -1


def _RoomVentilation(_phx_object: PHX.bldg_segment.Room) -> temp_RoomVentilation:
    """Find the Fresh-air Ventilator ID number which serves the PHX-Room"""

    wufi_object = temp_RoomVentilation()

    for mech_sys in _phx_object.mechanicals.systems:
        ventilator_type_number = 1
        for d in mech_sys.equipment_set.get_all_devices_by_type(ventilator_type_number):
            wufi_object.ventilator_id = d.id

    return wufi_object


@dataclass
class temp_UtilizationPattern_NonRes:
    absent_fac: int = 1
    m2_per_person: float = 0


def _UtilizationPattern_NonRes(_phx_object: UtilizationPattern_NonRes) -> temp_UtilizationPattern_NonRes:
    """Calculate the m2_per_person from the people_per_area for the PHX-Room"""

    wufi_object = temp_UtilizationPattern_NonRes()

    present_factor = float(_phx_object.occupancy.schedule.annual_utilization_factor)
    wufi_object.absent_fac = 1 - present_factor

    if _phx_object.occupancy.loads.people_per_area:
        wufi_object.m2_per_person = 1 / _phx_object.occupancy.loads.people_per_area

    return wufi_object


@dataclass
class temp_UtilizationPattern_Vent:
    remainder: float = 0


def _UtilizationPattern_Vent(_phx_object: UtilizationPattern_Vent) -> temp_UtilizationPattern_Vent:
    """Enforce 24 hour maximum DOS no matter what values are input."""

    wufi_object = temp_UtilizationPattern_Vent()

    a = round(_phx_object.utilization_rates.maximum.daily_op_sched, TOL)
    b = round(_phx_object.utilization_rates.standard.daily_op_sched, TOL)
    c = round(_phx_object.utilization_rates.basic.daily_op_sched, TOL)
    total = a + b + c

    wufi_object.remainder = round(24.0 - total, TOL)

    return wufi_object


@dataclass
class temp_Space:
    """PHX-Space, but with the Room level Programs"""

    space: PHX.spaces.Space
    ventilation: PHX.programs.ventilation.RoomVentilation
    lighting: PHX.programs.lighting.RoomLighting
    occupancy: PHX.programs.occupancy.RoomOccupancy
    elec_equipment: PHX.programs.electric_equipment.RoomElectricEquipment
    mechanicals: PHX.mechanicals.systems.Mechanicals
    space_percent_floor_area_total: float

    @property
    def peak_occupancy(self) -> float:
        return self.space.floor_area_weighted * self.occupancy.loads.people_per_area

    @property
    def total_space_elec_wattage(self) -> float:
        return self.space.floor_area_weighted * self.elec_equipment.loads.watts_per_area


@dataclass
class temp_Zone:
    """PHX-Zone with temp_Space objects"""

    spaces: list[temp_Space] = field(default_factory=list)


def _Zone(_phx_zone: PHX.bldg_segment.Zone) -> temp_Zone:
    """Since Program and Equipment are only present at the 'Room' level, need to add
    that info to the Spaces so that can be written out properly to WUFI.
    """

    temp_zone = temp_Zone()

    for room in _phx_zone.rooms:
        for base_space in room.spaces:
            # Calc % of total floor area, for lighting.
            # What the fuck WUFI???? You can't just use floor area?
            space_percent_floor_area_total = base_space.floor_area_weighted / _phx_zone.floor_area

            new_space = temp_Space(
                space=base_space,
                ventilation=room.ventilation,
                lighting=room.lighting,
                occupancy=room.occupancy,
                elec_equipment=room.electric_equipment,
                mechanicals=room.mechanicals,
                space_percent_floor_area_total=space_percent_floor_area_total,
            )

            # Preserve the Space-level flow rates, if they exist
            # instead of the Room-level flow rates
            if new_space.space.ventilation_loads:
                new_space.ventilation.loads.supply = base_space.ventilation_loads.supply
                new_space.ventilation.loads.extract = base_space.ventilation_loads.extract
                new_space.ventilation.loads.transfer = base_space.ventilation_loads.transfer

            temp_zone.spaces.append(new_space)

    return temp_zone


# Type Alias
temp_WUFI = Union[temp_RoomVentilation, temp_UtilizationPattern_NonRes, temp_UtilizationPattern_Vent, temp_Zone]
