# -*- coding: utf-8 -*-
# -*- Python Version: 3.x -*-

"""Function to locate the appropriate XML output Schema for the object """

import PyPH_WUFI.xml_schemas
import PyPH_WUFI.xml_node

from typing import Union

def xml_data(_object) -> list[Union[PyPH_WUFI.xml_node.XML_Node, PyPH_WUFI.xml_node.XML_List, PyPH_WUFI.xml_node.XML_Object]]:
    """Returns a list of the Object's Attributes in WUFI-XML format
    
    Returns:
    --------
        * (list): [
            XML_Node('IdentNr', 2),
            XML_Node('Name', 'My-Object'),
            ...
        ]
    """
    
    module = _object.__class__.__module__
    class_name = _object.__class__.__name__
    func = getattr(PyPH_WUFI.xml_schemas, '_{}'.format(class_name))
    return func(_object)