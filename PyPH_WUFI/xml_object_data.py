# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Function to locate the appropriate XML output Schema for the object """

import PyPH_WUFI.xml_schemas
import PyPH_WUFI.xml_node

from typing import Union


def xml_data(
    _object, _schema_name=None
) -> list[Union[PyPH_WUFI.xml_node.XML_Node, PyPH_WUFI.xml_node.XML_List, PyPH_WUFI.xml_node.XML_Object,]]:
    """Returns a list of the Object's Attributes in WUFI-XML format

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
            ...
        ]
    """
    if not _schema_name:
        module = _object.__class__.__module__
        class_name = _object.__class__.__name__
        func = getattr(PyPH_WUFI.xml_schemas, "_{}".format(class_name))
    else:
        func = getattr(PyPH_WUFI.xml_schemas, _schema_name)
    return func(_object)
