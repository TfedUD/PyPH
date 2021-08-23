"""Oganize and prepare the PHX file data for output"""


import PyPH_WUFI.type_collections
import PyPH_WUFI.utilization_patterns


def build_NonRes_utilization_patterns_from_zones(_zones: list):
    """

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
            util_collection.add_to_collection(util_pattern)

    return util_collection


def build_vent_utilization_patterns_from_zones(_zones: list):
    """

    Returns:
    --------
        * (PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes)
    """

    util_collection = PyPH_WUFI.type_collections.UtilPat_Collection_Ventilation()

    for zone in _zones:
        for space in zone.spaces:
            util_pattern = PyPH_WUFI.utilization_patterns.UtilizationPattern_Vent()

            util_pattern.OperatingDays = space.ventilation.utilization_pattern.OperatingDays

            util_collection.add_to_collection(util_pattern)

    return util_collection
