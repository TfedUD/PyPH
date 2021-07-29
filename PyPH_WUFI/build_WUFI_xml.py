# -*- coding: utf-8 -*-
# -*- Python Version: 3.x -*-

"""Functions used to create the full WUFI XML file"""

from typing import Any
from PHX.project import Project
from xml.dom.minidom import Document, Element
from .xml_node import XML_List, XML_Node, XML_Object
from .xml_object_data import xml_data

def _xml_str(_) -> str:
    """Util: Handle converting Boolean values to xml text format properly"""
    
    if isinstance(_, bool):
        if _:
            return 'true'
        else:
            return 'false'
    else:
        return str(_)

def _add_node_attributes(_data, _element) -> None:
    """Adds in any Node Attribure data, if any is found.
    
    Arguments:
    ----------
        * _data (XML_Node | XML_Object | XML_List): The XML Data object to use as the source
        * _elememt (xml.dom.minidom.Element): The element to set the Attributes for
    """
    
    if _data.attr_value is not None:
        _element.setAttributeNS(None, str(_data.attr_name), str(_data.attr_value))

def _add_text_node(_doc, _parent_node, _data) -> None:
    """Adds a basic text-node ie: <node_name>node_value</node_name> to the XML doc
    
    Arguments:
    ----------
        * _doc (xml.dom.minidom.doc): The XML document to operate on.
        * _parent_node (xml.dom.minidom.Element): The element to use as the 'parent' node.
        * _data (XML_Node): The data object to add.
    """
    
    txt = _doc.createTextNode( _xml_str(_data.node_value) )           # 1) Create the new text-node 
    el = _doc.createElementNS(None, _xml_str(_data.node_name))        # 2) Create a new Element
    el.appendChild(txt)                                               # 3) Add the text-node to the Element
    _add_node_attributes(_data, el)                                   # 4) Add the Optional Node Attributes
    _parent_node.appendChild(el)                                      # 5) Add the Element to the parent

def _add_children(_doc: Document, _parent_node: Element, _item) -> None:
    """Adds 'child' nodes to the document recursively.

    Will call the 'to_xml' property on any input objects and will walk through all the
    results including any lists or other Objects
    
    Arguments:
    ----------
        * _doc (xml.dom.minidom.doc): The XML document to operate on.
        * _parent_node (xml.dom.minidom.Element): The element to use as the 'parent' node.
        * _item (XML_Node | XML_Object | XML_List): The XML Data object to walk through
    """

    if isinstance(_item, XML_Node):
        #-- Basic Node, write out the value
        _add_text_node( _doc, _parent_node, _item )

    elif isinstance(_item, XML_Object):
        #-- Add a new node for the object, then try and add all its fields
        _new_parent_node = _doc.createElementNS(None, _xml_str(_item.node_name))
        _add_node_attributes(_item, _new_parent_node)
        _parent_node.appendChild(_new_parent_node) 

        for item in xml_data(_item.node_object):
            _add_children(_doc, _new_parent_node, item)

    elif isinstance(_item, XML_List):
        #-- Add a new node for the 'container', and then add each item in the list
        _new_parent_node = _doc.createElementNS(None, _xml_str(_item.node_name))
        _add_node_attributes(_item, _new_parent_node)
        _parent_node.appendChild(_new_parent_node)
        
        for each_item in _item.node_items:
            _add_children(_doc, _new_parent_node, each_item)

def create_project_xml_text(_project: Project) -> str:
    """Create all the XML Nodes as text for the input Project
    
    Arguments:
    ----------
        * _project (PyPH_WUFI.project.Project): the Project object to use as the 'source'

    Returns:
    --------
        * (str) The XML Nodes as Text
    """
    print('- '*50)
    print('writing out to xml.....')
    doc = Document()

    root = doc.createElementNS(None, 'WUFIplusProject')
    doc.appendChild(root)
    
    for item in xml_data(_project):
        _add_children(doc, root, item)

    return doc.toprettyxml()

def write_Project_to_wp_xml_file(_file_address, _Project) -> None:
    """Main: Write the 'Project' out to file as XML
    
    Arguments:
    ----------
        * _file_address (str): The file path to save to
        * _Project (PyPH_WUFI.project.Project): The Project Object to write to XML
    """

    xml_text = create_project_xml_text( _Project )
    with open(_file_address, 'w') as f:
        f.writelines(xml_text)
    
    print('Done.')