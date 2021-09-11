"""Oganize and prepare some WUFI-XML-Specific data formats / objects."""

import PyPH_WUFI.type_collections
import PyPH_WUFI.utilization_patterns
import PHX.bldg_segment


def build_NonRes_utilization_patterns_from_zones(_zones: list[PHX.bldg_segment.Zone]):
    """Collects and builds the Non-Res Utilization Patterns (occupancy, lighting) found on the Zone's Spaces

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes)
    """
    util_collection = PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes()

    for zone in _zones:
        for space in zone.spaces:
            util_pattern = PyPH_WUFI.utilization_patterns.UtilizationPattern_NonRes()
            util_pattern.occupancy = space.occupancy
            util_pattern.lighting = space.lighting
            pattern_id = util_pattern.occupancy.unique_key + util_pattern.lighting.unique_key

            util_collection.add_to_collection(util_pattern, _key=pattern_id, _reset_count=True)
            space.occupancy.id = util_pattern.id
            space.lighting.id = util_pattern.id

    return util_collection


def build_vent_utilization_patterns_from_zones(_zones: list[PHX.bldg_segment.Zone]):
    """Collects and builds the Ventilation Utilization Patterns found on the Zone's Spaces

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes)
    """

    # Create the new Util Pattern Collection
    util_collection = PyPH_WUFI.type_collections.UtilPat_Collection_Ventilation()

    for zone in _zones:
        for space in zone.spaces:
            # Get the Utilization from the Space, add it to the collection
            util_pattern = PyPH_WUFI.utilization_patterns.UtilizationPattern_Vent()

            util_pattern.name = space.ventilation.utilization.name
            util_pattern.operating_days = space.ventilation.utilization.operating_days
            util_pattern.operating_weeks = space.ventilation.utilization.operating_days
            util_pattern.utilization_rates = space.ventilation.utilization.utilization_rates

            key = space.ventilation.utilization.identifier
            util_collection.add_to_collection(util_pattern, _key=key, _reset_count=True)

    return util_collection