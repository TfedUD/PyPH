# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to oganize and prepare PHX Objects for WUFI-XML export"""

from typing import Optional
import PyPH_WUFI.WUFI_xml_schemas_write
import PyPH_WUFI.WUFI_xml_conversion_functions
from PyPH_WUFI.WUFI_xml_conversion_classes import temp_WUFI
from PyPH_WUFI.xml_node import xml_writable
from PHX._base import _Base as PHX_Base


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
        * Optional[PyPH_WUFI.WUFI_xml_conversion_functions.temp_WUFI]: A WUFI dataclass
            object with custom attributes to supplement the PHX object.
    """

    # -- Sort out the right converstion function name to look for
    if not _schema_nm:
        phx_obj_name = _phx_object.__class__.__name__
        _schema_nm = f"_{phx_obj_name}"

    # -- Get and execute the conversion function
    converter_function = getattr(PyPH_WUFI.WUFI_xml_conversion_functions, _schema_nm, None)
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
