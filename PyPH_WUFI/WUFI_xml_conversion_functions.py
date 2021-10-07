# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to convert data from PHX objects into WUFI-specific format.

These functions get called before the object is passed to the XML-Schema
and will construct all the required 'temp' objects needed in order to 
re-organize the PHX objects into WUFI-compatible shape.

Each function here should have a name which matches the PHX class name, 
preceeded by an undrscore: "_" ie: Room --> "_Room".
"""

import PHX.bldg_segment
from PyPH_WUFI.WUFI_xml_conversion_classes import (
    UtilizationPattern_Vent,
    UtilizationPatternCollection_Vent,
    UtilizationPattern_NonRes,
    UtilizationPatternCollection_NonRes,
    temp_RoomVentilation,
    temp_Space,
    temp_Zone,
    temp_Project,
)

TOL = 2  # Value tolerance for rounding. ie; 9.84318191919 -> 9.84

# ------------------------------------------------------------------------------
# -- HRV ID
def _RoomVentilation(_phx_object: PHX.bldg_segment.Room) -> temp_RoomVentilation:
    """Find the Fresh-air Ventilator ID number which serves the PHX-Room"""

    wufi_object = temp_RoomVentilation()

    for mech_sys in _phx_object.mechanicals.systems:
        ventilator_type_number = 1
        for d in mech_sys.equipment_set.get_all_devices_by_type(ventilator_type_number):
            wufi_object.ventilator_id = d.id

    return wufi_object


# ------------------------------------------------------------------------------
# -- Build all the Spaces with the Room Program attributes
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


# ------------------------------------------------------------------------------
# -- Project, Utilization Factors
def _build_NonRes_UtilCollection_from_zones(_zones: list[PHX.bldg_segment.Zone]):
    """Collects and builds the Non-Res Utilization Patterns (occupancy, lighting) found on the Zone's Rooms

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the PHX-Zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes)
    """
    util_collection = UtilizationPatternCollection_NonRes()

    for zone in _zones:
        for room in zone.rooms:
            util_pattern = UtilizationPattern_NonRes()
            util_pattern.occupancy = room.occupancy
            util_pattern.lighting = room.lighting
            pattern_id = util_pattern.occupancy.unique_key + util_pattern.lighting.unique_key

            util_collection.add_to_collection(util_pattern, _key=pattern_id, _reset_count=True)
            room.occupancy.id = util_pattern.id
            room.lighting.id = util_pattern.id

    return util_collection


def _build_vent_UtilCollection_from_zones(_zones: list[PHX.bldg_segment.Zone]) -> UtilizationPatternCollection_Vent:
    """Collects and builds the Ventilation Utilization Patterns found on the Zone's Rooms

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the PHX-Zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (UtilizationPatternCollection_Vent)
    """

    # Create the new Util Pattern Collection
    util_collection = UtilizationPatternCollection_Vent()

    for zone in _zones:
        for room in zone.rooms:
            # Build the UtilizationPattern based on the Space, add it to the collection
            util_pattern = UtilizationPattern_Vent()

            util_pattern.name = room.ventilation.schedule.name
            util_pattern.operating_days = room.ventilation.schedule.operating_days
            util_pattern.operating_weeks = room.ventilation.schedule.operating_weeks
            util_pattern.utilization_rates = room.ventilation.schedule.utilization_rates

            util_pattern.force_max_utilization_hours(_max_hours=24.0)

            key = room.ventilation.schedule.identifier
            util_collection.add_to_collection(util_pattern, _key=key, _reset_count=True)
            room.ventilation.schedule.id = util_pattern.id  # Reset the Room Vent id to match

    return util_collection


def _Project(_phx_project: PHX.project.Project) -> temp_Project:
    """Create the WUFI 'Utilization Pattern' Collections from the schedules and loads"""

    temp_project = temp_Project()

    temp_project.util_pattern_collection_non_residential = _build_NonRes_UtilCollection_from_zones(_phx_project.zones)
    temp_project.util_pattern_collection_ventilation = _build_vent_UtilCollection_from_zones(_phx_project.zones)

    return temp_project
