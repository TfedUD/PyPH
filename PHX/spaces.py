# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Space (Room) and Floor Area (iCFA / TFA) Classes
"""

from ._base import _Base
from .serialization.from_dict import _FloorSegment, _Floor, _Volume, _Space

class FloorSegment(_Base):
    """An individual segment of floor area with some relevant attributes"""

    def __init__(self):
        super(FloorSegment, self).__init__()
        self.weighting_factor = 1
        self.floor_area_gross = None
        self.floor_area_weighted = None
        self.space_name = None
        self.space_number = None
        self.non_res_lighting = None
        self.non_res_motion = None
        self.non_res_usage = None
        self.ventilation_v_sup = 0.0
        self.ventilation_v_eta = 0.0
        self.ventilation_v_trans = 0.0
        self.geometry = []
        self.host_zone_identifier = None
    
    @classmethod
    def from_dict(cls, _dict):
        return _FloorSegment(cls, _dict)

    @property
    def display_name(self):
        return '{}-{}'.format(self.space_number, self.space_name)
    
    def __str__(self):
        return 'PHX_{}: {}'.format(self.__class__.__name__, self.display_name)

class Floor(_Base):
    """A single Volume's Floor, made of one or more FloorSegments """

    def __init__(self):
        super(Floor, self).__init__()
        self.floor_segments = []

        self.space_name = None
        self.space_number = None
        self.non_res_lighting = None
        self.non_res_motion = None
        self.non_res_usage = None
        self.ventilation_v_sup = 0.0
        self.ventilation_v_eta = 0.0
        self.ventilation_v_trans = 0.0
        self.host_zone_identifier = None
    
    @classmethod
    def from_dict(cls, _dict):
        return _Floor(cls, _dict)

    @property
    def display_name(self):
        return '{}-{}'.format(self.space_number, self.space_name)

    def add_new_floor_segment(self, _new_flr_seg):
        if not _new_flr_seg: return

        self.floor_segments.append(_new_flr_seg)

        self.space_number = self._join_string_values( _new_flr_seg, 'space_number')
        self.space_name = self._join_string_values( _new_flr_seg, 'space_name')
        
        self.non_res_lighting = self._join_string_values( _new_flr_seg, 'non_res_lighting')
        self.non_res_motion = self._join_string_values( _new_flr_seg, 'non_res_motion')
        self.non_res_usage = self._join_string_values( _new_flr_seg, 'non_res_usage')
        
        self.ventilation_v_sup = self._join_ventilation_values( _new_flr_seg, 'ventilation_v_sup')
        self.ventilation_v_eta = self._join_ventilation_values( _new_flr_seg, 'ventilation_v_eta')
        self.ventilation_v_trans = self._join_ventilation_values( _new_flr_seg, 'ventilation_v_trans')

        self.host_zone_identifier = self._join_string_values( _new_flr_seg, 'host_zone_identifier')
    
    @property
    def geometry(self):
        if not self.floor_segments: return []
        
        geom = []
        for floor_segment in self.floor_segments:
            geom.extend( floor_segment.geometry )
        return geom

    def _join_string_values(self, _new_flr_seg, _attr_name):
        """Helper Function: Clean join of string attribute values from two FloorSegment Attributes        
        
        Arguments:
        ----------
            * _new_flr_seg (FloorSegment): The FloorSegment to add Attributes from
            * _attr_name (str): The Attribute to join
        
        Returns:
        --------
            * (str): The joined value
        """
        
        attr_values = set()

        new_val = getattr(_new_flr_seg, _attr_name, None)
        if new_val == 'None':
            new_val = None
        attr_values.add(new_val)

        for each_flr_seg in self.floor_segments:
            exg_val = getattr(each_flr_seg, _attr_name, None)
            if exg_val == 'None':
                exg_val = None
            attr_values.add(exg_val)
        
        if len(attr_values) != 1:
            msg = 'Error adding new FloorSegment to {}: Multiple values for "{}" found on the input FloorSegments'\
                ' for Spaces: "{}" and ""'.format(self.display_name, _attr_name, self.display_name, _new_flr_seg.display_name)
            raise Exception(msg)
        
        return list(attr_values)[0]

    def _join_ventilation_values(self, _new_flr_seg, _attr_name):
        """Helper Function: Clean join of Ventilation flow-rate values from two different FloorSegments
        
        Arguments:
        ----------
            * other (FloorSegment): The FloorSegment to join with
            * _attr_name (str): The Attribute to join
        
        Returns:
        --------
            * (float): The joined value
        """
        vals = []
        
        vals.append( float(getattr(_new_flr_seg, _attr_name, 0.0)) )
        for each_flr_seg in self.floor_segments:
            vals.append( float(getattr(each_flr_seg, _attr_name, 0.0)) )
    
        return max(vals)
    
    def __str__(self):
        return 'PHX_{}: {} ({} FloorSegments)'.format(self.__class__.__name__, self.display_name, len(self.floor_segments))

class Volume(_Base):
    """A single Volume, with a single Floor"""

    def __init__(self):
        super(Volume, self).__init__()
        self.space_name = None
        self.space_number = None
        self.host_zone_identifier = None

        self.floor = None
        self.average_ceiling_height = 2.5
        self.volume_geometry = []
    
    @classmethod
    def from_dict(cls, _dict):
        return _Volume(cls, _dict)
    
    @property
    def display_name(self):
        return '{}-{}'.format(self.space_number, self.space_name)

    def add_Floor(self, _floor):
        """Adds a Floor Object to the Volume, sets the Volume's Attributes"""

        self.floor = _floor
        self.space_name = _floor.space_name
        self.space_number = _floor.space_number
        self.host_zone_identifier = _floor.host_zone_identifier

    def __str__(self):
        return 'PHX_{}: {} ({} FloorSegments)'.format(self.__class__.__name__, self.display_name, len(self.floor.floor_segments))

class Space(_Base):
    """
    The Space is the primary spatial unit for a Passive House. This would roughly 
    map to a 'Zone' in EnergyPlus or 'Room' in Honeybee. The main difference is
    that the 'Space' contains information on all its sub-areas (Volumes) and
    TFA/iCFA floor segments.

    Space_01
      |
      +-- Volume_01
      |     |
      |     +-- Floor
      |         |
      |         +--FloorSegement_01
      |         +--FloorSegement_02
      |
      +-- Volume_02
      |     |
      |     +-- Floor
      |         |
      |         +--FloorSegement_03
      |         +--FloorSegement_04
      .
    """

    def __init__(self):        
        super(Space, self).__init__()
        self.space_name = None
        self.space_number = None
        self.host_zone_identifier = None

        self.volumes = []

        self.occupancy = None
        self.equipment = None
        self.ventilation = None
 
    @classmethod
    def from_dict(cls, _dict):
        return _Space(cls, _dict)
       
    @property
    def display_name(self):
        return '{}-{}'.format(self.space_number, self.space_name)
    
    def add_new_volume(self, _new_volume):
        """Adds a new Volume onto the Space. Verifies that the names/numbers/hosts match
        
        Arguments:
        ---------
            * _new_volume (Volume): The new Volume object to add to the Space
        
        Returns:
        --------
            * None
        """
        
        if not self.space_name:
            self.space_name = _new_volume.space_name
        else:
            if self.space_name != _new_volume.space_name:
                raise Exception('Error: Cannot add Volume with name: "{}" to'\
                    'Volume with name: "{}"'.format(_new_volume.space_name, self.space_name))
        
        if not self.space_number:
            self.space_number = _new_volume.space_number
        else:
            if self.space_number != _new_volume.space_number:
                raise Exception('Error: Cannot add Volume with number: "{}" to'\
                    'Volume with number: "{}"'.format(_new_volume.space_number, self.space_number))
        
        if not self.host_zone_identifier:
            self.host_zone_identifier = _new_volume.host_zone_identifier
        else:
            if self.host_zone_identifier != _new_volume.host_zone_identifier:
                raise Exception('Error: Cannot add Volume with Host-Zone: "{}" to'\
                    'Volume with Host-Zone: "{}"'.format(_new_volume.host_zone_identifier, self.host_zone_identifier))

        self.volumes.append(_new_volume)
    
    def __str__(self):
        return 'PHX_{}: {} ({} Volumes)'.format(self.__class__.__name__, self.display_name, len(self.volumes))