# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to oganize and prepare PHX Objects for WUFI-XML export"""

from typing import Optional
from PyPH_WUFI.type_collections import UtilizationPatternCollection_PH_NonRes, UtilPat_Collection_Ventilation
from PyPH_WUFI.utilization_patterns import UtilizationPattern_NonRes, UtilizationPattern_Vent
import PHX.bldg_segment
import PyPH_WUFI.WUFI_xml_schemas_write
import PyPH_WUFI.WUFI_xml_schemas_conversion
from PyPH_WUFI.WUFI_xml_schemas_conversion import temp_WUFI
from PyPH_WUFI.xml_node import xml_writable
from PHX._base import _Base as PHX_Base

# --
def build_NonRes_schedules_from_zones(_zones: list[PHX.bldg_segment.Zone]) -> UtilizationPatternCollection_PH_NonRes:
    """Collects and builds the Non-Res Utilization Patterns (occupancy, lighting) found on the Zone's Rooms

    Arguments:
    ----------
        _zones (list[PHX.bldg_segment.Zone]): A list of the PHX-Zones to collect the
            utilization patterns from.

    Returns:
    --------
        * (PyPH_WUFI.type_collections.UtilizationPatternCollection_PH_NonRes)
    """
    util_collection = UtilizationPatternCollection_PH_NonRes()

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


def build_Vent_Schdeules_from_zones(_zones: list[PHX.bldg_segment.Zone]) -> UtilPat_Collection_Ventilation:
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
    util_collection = UtilPat_Collection_Ventilation()

    for zone in _zones:
        for room in zone.rooms:
            # Build the UtilizationPattern based on the Space, add it to the collection
            util_pattern = UtilizationPattern_Vent()

            util_pattern.name = room.ventilation.schedule.name
            util_pattern.operating_days = room.ventilation.schedule.operating_days
            util_pattern.operating_weeks = room.ventilation.schedule.operating_weeks
            util_pattern.utilization_rates = room.ventilation.schedule.utilization_rates

            key = room.ventilation.schedule.identifier
            util_collection.add_to_collection(util_pattern, _key=key, _reset_count=True)
            room.ventilation.schedule.id = util_pattern.id  # Reset the Room Vent id to match

    return util_collection


# --
def create_WUFI_object_from_phx(_phx_object: PHX_Base, _schema_nm: str = None) -> Optional[temp_WUFI]:
    """Returns a new temporary object with WUFI-specific data and attributes, or None
    if no converter is found for the Object. These converter functions are used when
    the WUFI model structure is significantly different than the PHX structure. Rather
    than modify / add / edit the attrs on the PHX object itself, these 'special' WUFI
    object fields are bundled in this custom object. This is done to ensure that
    the 'writing' of the PHX to file doesn't modify the PHX objects themselves.

    This special 'temporary' object can then be passed to the xml_schema function
    alongside the base PHX object and will supplement the PHX object data where relevant.

    Arguments:
    ----------
        * _phx_object (PHX._base._Base): The PHX Object to find the converter function for.
        * _schema_nm (str | None): Optional converter schema name to use for lookup.

    Returns:
    --------
        * Optional[PyPH_WUFI.WUFI_xml_schemas_conversion.temp_WUFI]: A WUFI dataclass
            object with custom attributes to supplement the PHX object.
    """

    # -- Sort out the right converstion function name to look for
    if not _schema_nm:
        phx_obj_name = _phx_object.__class__.__name__
        _schema_nm = f"_{phx_obj_name}"

    # -- Get and execute the conversion function
    converter_function = getattr(PyPH_WUFI.WUFI_xml_schemas_conversion, _schema_nm, None)
    if converter_function:
        wufi_object = converter_function(_phx_object)
        return wufi_object

    # -- If no 'converter' for the object is found, return None
    return None


def get_PHX_object_as_xml_node_list(_phx_object: PHX_Base, _schema_nm: str = None) -> list[xml_writable]:
    """Returns a list of the Object's Attributes in WUFI-XML format

    Used to locate the appropriate XML output Schema for the object.

    Arguments:
    ----------
        * _phx_object (PHX._base._Base): The PHX Object to go find the WUFI-XML data schema for. By default,
            will use the name of the object's class preceded by an underscore. ie:
            "Room" will seach the xml_schemas for a function named "_Room"
        * _schema_nm (str | None): Optional schema-name to search for.

    Returns:
    --------
        * list[PyPH_WUFI.xml_node.xml_writable]:

        ie: [
            XML_Node('IdentNr', 2),
            XML_Node('Name', 'My-Object'),
            XML_List( ... ),
            ...
            ]
    """

    # -- Figure out the right XML Write Schema to use
    if not _schema_nm:
        class_name = _phx_object.__class__.__name__
        _schema_nm = "_{}".format(class_name)

    # -- Get WUFI-Specific / Special object with custom attrs and structure
    wufi_object = create_WUFI_object_from_phx(_phx_object, _schema_nm)

    # -- Convert the object to an XML Node List
    xml_schema_function = getattr(PyPH_WUFI.WUFI_xml_schemas_write, _schema_nm)
    xml_node_list = xml_schema_function(_phx_object, wufi_object)

    return xml_node_list
