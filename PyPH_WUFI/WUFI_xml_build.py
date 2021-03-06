# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions used to create the full WUFI XML file"""

import logging
from typing import Union
from xml.dom.minidom import Document, Element

import PHX.project
import PyPH_WUFI.xml_node
import PyPH_WUFI.WUFI_xml_convert_phx

logging.basicConfig(filename="sample/EM_logs/example.log", filemode="w", encoding="utf-8", level=logging.DEBUG)


def _xml_str(_: Union[str, bool]) -> str:
    """Util: Handle converting Boolean values to xml text format properly"""

    if isinstance(_, bool):
        if _:
            return "true"
        else:
            return "false"
    else:
        return str(_)


def _add_node_attributes(_data: PyPH_WUFI.xml_node.xml_writable, _element: Element) -> None:
    """Sets in any Node Attribute data on the Element, if any is found.

    Arguments:
    ----------
        * _data (PyPH_WUFI.xml_node.xml_writable): The XML Data object to use as the source
        * _elememt (xml.dom.minidom.Element): The XML Element to set the Attributes for.
    """

    if _data.attr_value is not None:
        _element.setAttributeNS(None, str(_data.attr_name), str(_data.attr_value))


def _add_text_node(_doc: Document, _parent_node: Element, _data: PyPH_WUFI.xml_node.XML_Node) -> None:
    """Adds a basic text-node ie: "<node_name>node_value</node_name>" to the XML Parent Node.

    Arguments:
    ----------
        * _doc (xml.dom.minidom.Document): The XML document to operate on.
        * _parent_node (xml.dom.minidom.Element): The XML element to use as the 'parent' node.
        * _data (PyPH_WUFI.xml_node.XML_Node): The new XML_Node object to add to the 'parent' node.
    """

    txt = _doc.createTextNode(_xml_str(_data.node_value))  # 1) Create the new text-node
    el = _doc.createElementNS(None, _xml_str(_data.node_name))  # 2) Create a new Element
    el.appendChild(txt)  # 3) Add the text-node to the Element
    _add_node_attributes(_data, el)  # 4) Add the Optional Node Attributes
    _parent_node.appendChild(el)  # 5) Add the Element to the parent


def _add_children(_doc: Document, _parent_node: Element, _item: PyPH_WUFI.xml_node.xml_writable) -> None:
    """Adds 'child' nodes to the document recursively.

    Will call PyPH_WUFI.phx_converters..get_PHX_object_as_xml_node_list() function on any input
    objects and will walk through all the resulting lists or Objects recursively.

    Arguments:
    ----------
        * _doc (xml.dom.minidom.doc): The XML document to operate on.
        * _parent_node (xml.dom.minidom.Element): The element to use as the 'parent' node.
        * _item (PyPH_WUFI.xml_node.XML_Node | PyPH_WUFI.xml_node.XML_Object |
            PyPH_WUFI.xml_node.XML_List): The XML Data object to walk through.
    """

    if isinstance(_item, PyPH_WUFI.xml_node.XML_Node):
        # -- Basic Node, write out the value
        _add_text_node(_doc, _parent_node, _item)

    elif isinstance(_item, PyPH_WUFI.xml_node.XML_Object):
        # -- Add a new node for the object, then try and add all its fields
        _new_parent_node = _doc.createElementNS(None, _xml_str(_item.node_name))
        _add_node_attributes(_item, _new_parent_node)
        _parent_node.appendChild(_new_parent_node)

        for item in PyPH_WUFI.WUFI_xml_convert_phx.get_PHX_object_as_xml_node_list(
            _item.node_object, _item.schema_name
        ):
            _add_children(_doc, _new_parent_node, item)

    elif isinstance(_item, PyPH_WUFI.xml_node.XML_List):
        # -- Add a new node for the 'container', and then add each item in the list
        _new_parent_node = _doc.createElementNS(None, _xml_str(_item.node_name))
        _add_node_attributes(_item, _new_parent_node)
        _parent_node.appendChild(_new_parent_node)

        for each_item in _item.node_items:
            _add_children(_doc, _new_parent_node, each_item)


def create_project_xml_text(_project: PHX.project.Project) -> str:
    """Create all the XML Nodes as text for the input Project

    Arguments:
    ----------
        * _project (PHX.project.Project): the Project object to use as the 'source'
            for the xml text.

    Returns:
    --------
        * (str) The XML Nodes as text.
    """
    doc = Document()

    root = doc.createElementNS(None, "WUFIplusProject")
    doc.appendChild(root)

    for item in PyPH_WUFI.WUFI_xml_convert_phx.get_PHX_object_as_xml_node_list(_project):
        _add_children(doc, root, item)

    return doc.toprettyxml()
