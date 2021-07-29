# -*- coding: utf-8 -*-
# -*- Python Version: 3.x -*-

"""For XML Objects with constrained Attributes, used to organize and validate names/values

During XML write, these objects will look to the "selection_options" module to 
see what options are 'valid' and to align attr-names and attr-values. 
"""

from . import selection_options

class SelectionInputTypeError(Exception):
    def __init__(self, _name, _in):
        self.message = f'Error: Input to "{_name}" must be Integer value. Got: "{_in}", type: {type(_in)}.'
        super().__init__(self.message)

class SelectionInputValueError(Exception):
    def __init__(self, _name, _in, _allowable_ins):
        self.message = f'Selection for "{_name}" set to: "{_in}". Please set to only: {_allowable_ins}'
        super().__init__(self.message)

class Selection:

    def __init__(self, _node_name, _node_value):
        self.parent_name, self.node_name = _node_name.split('::')
        self.attr_data = self.get_attribute_data(_node_name)
        self.node_value = self.validate_input(_node_value)
        
        self.attr_name = self.attr_data.get('attr_name')
        self.attr_value = self.attr_data.get('enum').get(self.node_value)
    
    def get_attribute_data(self, _node_name):
        """Get the right data dict from the selection_options module"""

        d = getattr(selection_options, f'__{self.parent_name}', {}).get(self.node_name, {})
        
        if not d: raise Exception('Error: Cannot find data for Node: "{}"?'.format(self._node_name))
        else: return d

    def validate_input(self, _input):
        """Ensure that the input is allowed / valid"""
        #--- Use a Default, first in the options list of keys
        if _input is None: _input = list(self.attr_data.get('enum').keys())[0]

        #--- Validate input type
        try: val = int( _input )
        except: raise SelectionInputTypeError(self.node_name, _input)

        #--- Validate input is one of the allowable options
        allowable_inputs = list(self.attr_data.get('enum', {}).keys())
        if val not in allowable_inputs: raise SelectionInputValueError(self.node_name, _input, allowable_inputs)
        else: return val

    @property
    def xml_data(self):
        return (self.node_name, self.node_value, self.attr_name, self.attr_value)

