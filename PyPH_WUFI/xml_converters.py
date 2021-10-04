# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to prepare PHX objects for WUFI export"""

import PyPH_WUFI.xml_schemas
import PyPH_WUFI.xml_node

from typing import Any, Optional


def prepare_obj_for_WUFI(_object: Any, _schema_name: Optional[str] = None):
    """Will reorganize PHX data structure to align with the WUFI structure and data formats.

    This conversion should be called before sending the object out to the get_object_as_xml_list() function

    Arguments:
    ----------
        * _object (any): The PHX object to use as the source.
        * _ schema_name (str | None): Optional name for the schema_name to lookup.
            If None, will use the object's name preceeded by an underscore (ie: Floor -> "_Floor")

    Returns:
    --------
        * The input object, modified to match the WUFI structure as needed
    """

    class_name = _object.__class__.__name__
    search_name = "_{}".format(class_name)
    # Find the right converter function (someplace?)
    # Execute it, get the results
    # func = getattr(search_name)

    return _object, _schema_name
    # if func:
    #     return func(_object)
    # else:
    #     return _object


def get_object_as_xml_list(_object: Any, _schema_name: Optional[str] = None) -> list[PyPH_WUFI.xml_node.xml_writable]:
    """Returns a list of the Object's Attributes in WUFI-XML format

    Used to locate the appropriate XML output Schema for the object.

    Arguments:
    ----------
        * _object (Any): The WUFI Object to go find the XML data schema for. By default,
            will use the name of the object's class preceded by an underscore. ie:
            "Room" will seach the xml_schemas for a function named "_Room"
        * _schema_name (str | None): Optional function name to seach the xml_schema
            list for. If None is input, will use the Object's name as the seach key.

    Returns:
    --------
        * (list): [
            XML_Node('IdentNr', 2),
            XML_Node('Name', 'My-Object'),
            XML_List( ... ),
            ...
        ]
    """
    if not _schema_name:
        class_name = _object.__class__.__name__
        search_name = "_{}".format(class_name)
        func = getattr(PyPH_WUFI.xml_schemas, search_name)
    else:
        func = getattr(PyPH_WUFI.xml_schemas, _schema_name)
    return func(_object)
