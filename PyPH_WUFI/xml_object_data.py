# -*- coding: utf-8 -*-
# -*- Python Version: 3.x -*-

"""Function to locate the appropriate XML output Schema for the object """

from . import xml_schemas
from .xml_node import XML_Node, XML_List, XML_Object
from typing import Union

def xml_data(_object) -> list[Union[XML_Node, XML_List, XML_Object]]:
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
    func = getattr(xml_schemas, '_{}'.format(class_name))
    return func(_object)