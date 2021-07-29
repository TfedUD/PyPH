# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Geometry Classes
"""

from ._base import _Base
from ladybug_geometry.geometry3d.face import Face3D

def LBT_geometry_dict_util(_dict):
    """Utility for de-serializing Ladybug Geometry dictionaries
    
    Arguments:
    ----------
        * _dict (dict): The dictionary for the object to try and convert to live LBT Geometry Object(s)

    Returns:
    --------
        * LBT Geometry
    """
    
    object_type = _dict.get('type', None)
    assert object_type is not None, 'Error converting to LBT Geometry: No "type" '\
                                    'information found in the input dictionary?'
    
    if str(object_type) == 'Face3D':
        new_obj = Face3D.from_dict(_dict)
    else:
        new_obj = None
        raise Exception('Error: Cannot convert LBT Geometry of type: "{}"'.format(str(object_type)))

    return new_obj

class Vector(_Base):
    """Simple Vector class used to represent Surface Normal
    
    Attributes:
    -----------
        * x (float):
        * y (float):
        * z (float):
    """

    def __init__(self):
        super(Vector, self).__init__()
        self.x = 0
        self.y = 0
        self.z = 0  

class Vertex(_Base):
    """ A single Vertex object with x, y, z positions and an ID number

    Will keep a running tally as objects are created, increments in the 'id'
    attribute.
    
    Attributes:
    -----------
        * id (int): The running tally of number of objects created
        * x (float): x position
        * y (float): y position
        * z (float): z position
    """

    _count = 0

    def __init__(self):       
        super(Vertex, self).__init__()
        self.id = self._count
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(Vertex, cls).__new__(cls, *args, **kwargs)

class Polygon(_Base):
    """A Single Polygon Object, part of a Component
    
    Attributes:
    -----------
        * id (int): Polygon id number
        * nVec (Vector): The Polygon surface normal Vector
        * idPolyI (list):
        * idVert (list[int]): A list of the Polygon's Vertices' ID numbers
        * vertices (list[Vertex]): The Polygon's Vertices in a list
        * children (list[int]): A list of the Child Poly IdentNrs (ie: for Windows)
    """

    _count = 10000000-1

    def __init__(self):
        super(Polygon, self).__init__()
        self.id = self._count
        self._nVec = None
        self.idPolyI = []
        self.vertices = []
        self.children = [] # IdentNr of the children

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        
        cls._count += 1
        return super(Polygon, cls).__new__(cls, *args, **kwargs)

    @property
    def nVec(self):
        """Surface Normal
        
        Returns:
        --------
            * (Vector): The polygon's Surface Normal
        """
        return self._nVec

    @nVec.setter
    def nVec(self, _in):
        if not hasattr(_in, 'x') or not hasattr(_in, 'y') or not hasattr(_in, 'z'):
            msg = 'Error: The "nVec" input should be a Vector with'\
                'x,y,z attributes. Got "{}", type: {type(_in_)}'.format(_in)
            raise Exception(msg)
        
        self._nVec = _in
    
    @property
    def idVert(self):
        """ 
        Returns:
        --------
            * list[int]: A list of the Polygon's Vertex ID numbers
        """
        return [ vert.id for vert in self.vertices ]

    def add_children(self, _child_polys):
        """ Adds new child Poly IdentNrs to the 'children' list
        
        Arguments:
        ----------
            * _child_polys (list[Polygon]): A list of Poly objects to add as children (ie: for Windows)
        """
        if not _child_polys: return

        if not isinstance(_child_polys, list):
            _child_polys = [ _child_polys ]

        self.children.extend( [ _.id for _ in _child_polys ] )

class Geom(_Base):
    """Geometry Collection"""

    def __init__(self):
        super(Geom, self).__init__()
        self.polygons = []
    
    @property
    def vertices(self):
        return (v for p in self.polygons for v in p.vertices)

    def add_component_polygons( self, _compos):
        """Adds component's polygons to the Geometry's 'polygons' list
        
        Arguments:
        ----------
            * _compos (Component): The components to add the polygons from
        """
        
        if not isinstance(_compos, list):
            _compos = [ _compos ]

        for compo in _compos:
            for poly in compo.polygons:
                self.polygons.append( poly )


