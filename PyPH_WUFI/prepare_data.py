"""Oganize and prepare some WUFI-XML-Specific data formats / objects."""

import PyPH_WUFI.type_collections
import PyPH_WUFI.utilization_patterns
import PHX.bldg_segment


def build_NonRes_schedules_from_zones(_zones: list[PHX.bldg_segment.Zone]):
    """Collects and builds the Non-Res Utilization Patterns (occupancy, lighting) found on the Zone's Rooms

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the PHX-Zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes)
    """
    util_collection = PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes()

    for zone in _zones:
        for room in zone.rooms:
            util_pattern = PyPH_WUFI.utilization_patterns.UtilizationPattern_NonRes()
            util_pattern.occupancy = room.occupancy
            util_pattern.lighting = room.lighting
            pattern_id = util_pattern.occupancy.unique_key + util_pattern.lighting.unique_key

            util_collection.add_to_collection(util_pattern, _key=pattern_id, _reset_count=True)
            room.occupancy.id = util_pattern.id
            room.lighting.id = util_pattern.id

    return util_collection


def build_Vent_Schdeules_from_zones(_zones: list[PHX.bldg_segment.Zone]):
    """Collects and builds the Ventilation Utilization Patterns found on the Zone's Rooms

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the PHX-Zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (PyPH_WUFI.type_collections.UtilizationPattern_Vent)
    """

    # Create the new Util Pattern Collection
    util_collection = PyPH_WUFI.type_collections.UtilPat_Collection_Ventilation()

    for zone in _zones:
        for room in zone.rooms:
            # Get the Utilization from the Space, add it to the collection
            util_pattern = PyPH_WUFI.utilization_patterns.UtilizationPattern_Vent()

            util_pattern.name = room.ventilation.schedule.name
            util_pattern.operating_days = room.ventilation.schedule.operating_days
            util_pattern.operating_weeks = room.ventilation.schedule.operating_weeks
            util_pattern.utilization_rates = room.ventilation.schedule.utilization_rates

            key = room.ventilation.schedule.identifier
            util_collection.add_to_collection(util_pattern, _key=key, _reset_count=True)

    return util_collection
