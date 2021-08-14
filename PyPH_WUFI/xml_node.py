# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Classes used to build XML Node Objects which are used during XML Output"""


class XML_Node:
    """A single node text/numeric item. Optional Attribute data"""

    def __init__(self, _node_name, _node_value, _attr_name=None, _attr_value=None):
        self.node_name = _node_name
        self.node_value = _node_value
        self.attr_name = _attr_name
        self.attr_value = _attr_value


class XML_List:
    """A List of XML Writable objects. Used to add 'count' info to the list parent node"""

    def __init__(self, _node_name, _node_items, _attr_name="count", _attr_value=None):
        self.node_name = _node_name
        self.node_items = _node_items
        self.attr_name = _attr_name
        self._attr_value = _attr_value

    @property
    def attr_value(self):
        if self._attr_value is not None:
            return self._attr_value
        else:
            return len(self.node_items)

    @attr_value.setter
    def attr_value(self, _in):
        self._attr_value = _in


class XML_Object:
    """XML Writable Object. Object fields will be writen out as child nodes"""

    def __init__(self, _node_name, _node_object, _attr_name=None, _attr_value=None):
        self.node_name = _node_name
        self.node_object = _node_object
        self.attr_name = _attr_name
        self.attr_value = _attr_value
