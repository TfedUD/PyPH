# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Temporary Classes used during XML write to store extra / non-PHX data which is needed by WUFI.

These classes also allow for the reorganization of the PHX model elements into WUFI structure.
"""

from collections import defaultdict
from typing import Union
from dataclasses import dataclass, field

import PHX.spaces
import PHX.programs.schedules
import PHX.programs.lighting
import PHX.programs.occupancy
import PHX.programs.ventilation
import PHX.programs.electric_equipment
import PHX.bldg_segment
import PHX.mechanicals.systems

import PyPH_WUFI.type_collections

# ------------------------------------------------------------------------------
class UtilizationPattern_NonRes:
    """WUFI Style Utilization Pattern for Non-Residential"""

    _count = 0

    def __init__(self):
        self._id = self._count
        self.occupancy = None
        self.lighting = None

    @property
    def relative_absence_factor(self):
        if self.occupancy is None or self.occupancy.schedule is None:
            return 1
        return 1.0 - float(self.occupancy.schedule.relative_utilization_factor)

    @property
    def m2_per_person(self):
        if self.occupancy is None or self.occupancy.loads is None:
            return 0

        if self.occupancy.loads.people_per_area == 0:
            return 0

        return 1 / self.occupancy.loads.people_per_area

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(UtilizationPattern_NonRes, cls).__new__(cls, *args, **kwargs)


class UtilizationPatternCollection_NonRes(PyPH_WUFI.type_collections.Collection):
    def __init__(self):
        super(UtilizationPatternCollection_NonRes, self).__init__()
        self._allowed_types = UtilizationPattern_NonRes


class UtilizationPattern_Vent:
    """WUFI Style Utilization Pattern for Ventilation"""

    _count = 0

    def __init__(self):
        self.id: int = self._count
        self.name: str = None
        self.operating_days: float = None
        self.operating_weeks: float = None
        self.utilization_rates: PHX.programs.schedules.Vent_UtilRates = PHX.programs.schedules.Vent_UtilRates()

    def force_max_utilization_hours(self, _max_hours: float = 24.0) -> None:
        """Ensure that the total utilization hours never exceed target (default=24).
        Will adjust the minimum daily_op_sched as needed.
        """

        tolerance = 2

        a = round(self.utilization_rates.maximum.daily_op_sched, tolerance)
        b = round(self.utilization_rates.standard.daily_op_sched, tolerance)
        c = round(self.utilization_rates.basic.daily_op_sched, tolerance)
        total = a + b + c

        self.utilization_rates.minimum.daily_op_sched = round(_max_hours - total, tolerance)

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(UtilizationPattern_Vent, cls).__new__(cls, *args, **kwargs)


class UtilizationPatternCollection_Vent(PyPH_WUFI.type_collections.Collection):
    def __init__(self):
        super(UtilizationPatternCollection_Vent, self).__init__()
        self._allowed_types = UtilizationPattern_Vent


# ------------------------------------------------------------------------------
@dataclass
class temp_RoomVentilation:
    ventilator_id: int = -1


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


@dataclass
class temp_Project:
    """PHX Project with WUFI 'Utilization Patterns' which are kinda like Schedules, except weirder."""

    util_pattern_collection_non_residential: UtilizationPatternCollection_NonRes = (
        UtilizationPatternCollection_NonRes()
    )
    util_pattern_collection_ventilation: UtilizationPatternCollection_Vent = UtilizationPatternCollection_Vent()


# ------------------------------------------------------------------------------
class temp_Mechanicals:
    def __init__(self):
        self._mech_groups = defaultdict(list)

    @property
    def mech_groups(self):
        return self._mech_groups.values()


@dataclass
class temp_MechanicalSystemsGroup:
    """Reorganize Mechanicals into groups, so it matches the WUFI format"""

    wufi_devices: list = field(default_factory=list)
    group_type_number: int = 1


@dataclass
class temp_MechanicalDevice:
    """A WUFI 'Device' which is one part of a larger 'SystemGroup'"""

    name: str = ""
    id: int = 1
    device: None = None
    device_type: int = 1
    system_type: int = 1
    system_usage: PHX.mechanicals.systems.HVAC_System_Usage = PHX.mechanicals.systems.HVAC_System_Usage()
    properties: None = None


# ------------------------------------------------------------------------------
@dataclass
class temp_PH_Climate:
    """WUFI breaks off PH Cliamte data into its own section"""

    location = None
    ground = None
    summer_daily_temperature_swing = None
    average_wind_speed = None

    monthly_temperature_air = None
    monthly_temperature_dewpoint = None
    monthly_temperature_sky = None
    monthly_temperature_ground = None

    monthly_radiation_north = None
    monthly_radiation_east = None
    monthly_radiation_south = None
    monthly_radiation_west = None
    monthly_radiation_global = None

    peak_heating_1 = None
    peak_heating_2 = None
    peak_cooling = None


@dataclass
class temp_Climate:
    PH_Climate = temp_PH_Climate()


# ------------------------------------------------------------------------------
@dataclass
class temp_Building:
    numerics: None = None
    airflow_model: None = None
    count_generator: None = None
    has_been_generated: None = None
    has_been_changed_since_last_gen: None = None
    components: None = None
    zones: None = None


@dataclass
class temp_PH_Building_Internal_Gains_Data:
    int_gains_evap_per_person: float = 0.0
    int_gains_flush_heat_loss: float = 0.0
    int_gains_num_toilets: int = 0
    int_gains_toilet_room_util_pat: int = 0
    int_gains_use_school_defaults: int = 0
    int_gains_dhw_marginal_perf_ratio: int = 0


@dataclass
class temp_PH_Building_Internal_Gains:
    data = temp_PH_Building_Internal_Gains_Data()


@dataclass
class temp_PH_Building:
    id: int = 0
    occupancy_category: int = 0
    occupancy_type: int = 0
    building_status: int = 0
    building_type: int = 0
    occupancy_setting_method: int = 0
    num_units: int = 0
    num_stories: int = 0
    q50: float = 0
    n50: float = 0
    foundations: int = 0
    int_gains: temp_PH_Building_Internal_Gains = temp_PH_Building_Internal_Gains()
    summer_hrv_bypass_mode: int = 0


@dataclass
class temp_PassiveHouseData:
    certification_criteria: int = 0
    localization_selection_type: int = 0
    PHIUS2021_heating_demand: float = 0
    PHIUS2021_cooling_demand: float = 0
    PHIUS2021_heating_load: float = 0
    PHIUS2021_cooling_load: float = 0
    PH_Buildings: list = field(default_factory=list)


# Type Alias
temp_WUFI = Union[
    temp_PH_Climate,
    temp_Climate,
    temp_Project,
    temp_RoomVentilation,
    temp_Zone,
    temp_Space,
    temp_MechanicalSystemsGroup,
    temp_MechanicalDevice,
    temp_PH_Building,
    temp_Building,
    temp_PH_Building_Internal_Gains,
    temp_PH_Building_Internal_Gains_Data,
    temp_PassiveHouseData,
]
