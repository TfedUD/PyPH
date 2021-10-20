# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to oganize and prepare PHX Objects for WUFI-XML export"""

# from typing import Optional
from typing import Optional
import PyPH_WUFI.WUFI_xml_schemas_write
import PyPH_WUFI.WUFI_xml_conversion_functions

# from PyPH_WUFI.WUFI_xml_conversion_classes import temp_WUFI
from PyPH_WUFI.xml_node import xml_writable
from PHX._base import _Base as PHX_Base


def get_PHX_object_as_xml_node_list(_phx_object: PHX_Base, _schema_nm: Optional[str] = None) -> list[xml_writable]:
    """Returns a list of the Object's Attributes in WUFI-XML format

    Used to locate the appropriate XML output Schema for the object.

    Arguments:
    ----------
        * _phx_object (PHX._base._Base): The PHX Object to go find the WUFI-XML data schema for.
        * _schema_nm (str | None): Optional schema-name to search for. If None, by default,
            will use the name of the object's class preceded by an underscore. ie:
            "Room" will seach the xml_schemas for a function named "_Room"

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

    # -- Convert the object to an XML Node List
    xml_schema_function = getattr(PyPH_WUFI.WUFI_xml_schemas_write, _schema_nm)
    xml_node_list = xml_schema_function(_phx_object)

    return xml_node_list
