# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to collect / correct / convert data from PHX objects into WUFI-specific format"""

from dataclasses import dataclass, field
from typing import Union

import PHX.programs.schedules
import PHX.bldg_segment
import PyPH_WUFI.utilization_patterns

TOL = 2  # Value tolerance for rounding. ie; 9.84318191919 -> 9.84


@dataclass
class temp_RoomVentilation:
    ventilator_id: int = -1


def _RoomVentilation(_phx_object: PHX.bldg_segment.Room) -> temp_RoomVentilation:
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


def _UtilizationPattern_NonRes(
    _phx_object: PyPH_WUFI.utilization_patterns.UtilizationPattern_NonRes,
) -> temp_UtilizationPattern_NonRes:
    wufi_object = temp_UtilizationPattern_NonRes()

    present_factor = float(_phx_object.occupancy.schedule.annual_utilization_factor)
    wufi_object.absent_fac = 1 - present_factor

    if _phx_object.occupancy.loads.people_per_area:
        wufi_object.m2_per_person = 1 / _phx_object.occupancy.loads.people_per_area

    return wufi_object


@dataclass
class temp_UtilizationPattern_Vent:
    remainder: float = 0


def _UtilizationPattern_Vent(
    _phx_object: PyPH_WUFI.utilization_patterns.UtilizationPattern_Vent,
) -> temp_UtilizationPattern_Vent:
    wufi_object = temp_UtilizationPattern_Vent()

    # -- Enforce a 24 hour maximum, no matter what
    a = round(_phx_object.utilization_rates.maximum.daily_op_sched, TOL)
    b = round(_phx_object.utilization_rates.standard.daily_op_sched, TOL)
    c = round(_phx_object.utilization_rates.basic.daily_op_sched, TOL)
    total = a + b + c

    wufi_object.remainder = round(24.0 - total, TOL)

    return wufi_object


@dataclass
class temp_Space:
    """Space, but with the Room level Programs"""

    space = None
    ventilation = None
    lighting = None
    occupancy = None
    mechanicals = None

    @property
    def peak_occupancy(self) -> float:
        return self.space.floor_area_weighted * self.occupancy.loads.people_per_area


@dataclass
class temp_Zone:
    spaces: list[temp_Space] = field(default_factory=list)


def _Zone(_phx_object: PHX.bldg_segment.Zone) -> temp_Zone:
    """Since Program and Equipment are only present at the 'Room' level, need to add
    that info to the spaces so that can be written out properly to WUFI.
    """

    temp_zone = temp_Zone()

    for room in _phx_object.rooms:
        for base_space in room.spaces:
            new_space = temp_Space()
            new_space.space = base_space

            # -- Inherit Programs from Room
            new_space.ventilation = room.ventilation
            new_space.lighting = room.lighting
            new_space.occupancy = room.occupancy
            new_space.mechanicals = room.mechanicals

            # Preserve the Space-level flow rates, if they exist
            if new_space.space.ventilation_loads:
                new_space.ventilation.loads.supply = base_space.ventilation_loads.supply
                new_space.ventilation.loads.extract = base_space.ventilation_loads.extract
                new_space.ventilation.loads.transfer = base_space.ventilation_loads.transfer

            temp_zone.spaces.append(new_space)

    return temp_zone


temp_WUFI = Union[temp_RoomVentilation, temp_UtilizationPattern_NonRes, temp_UtilizationPattern_Vent, temp_Zone]
