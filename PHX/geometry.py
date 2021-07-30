# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Geometry Classes
"""

from ._base import _Base
from ladybug_geometry.geometry3d.face import Face3D
from .component import Component

class PolygonNormalError(Exception):
    def __init__(self, _in):
        self.message = f'Error: The Polygon "nVec" input should be a Vector with'\
                    f'x,y,z attributes. Instead, got "{_in}", type: "{type(_in)}"'
        super().__init__(self.message)

def LBT_geometry_dict_util(_dict):
    # type (dict): -> Optional[Face3D]
    """Utility for de-serializing Ladybug Geometry dictionaries
    
    Arguments:
    ----------
        * _dict (dict): The dictionary for the object to try and convert to live LBT Geometry Object(s)

    Returns:
    --------
        * Optional[Face3D]: The Ladybug Face3D Object
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

    def __init__(self, x=0.0, y=0.0, z=0.0):
        super(Vector, self).__init__()
        self.x = x
        self.y = y
        self.z = z 

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

    def __init__(self, x=0.0, y=0.0, z=0.0):       
        super(Vertex, self).__init__()
        self.id = self._count
        self.x = x
        self.y = y
        self.z = z

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
            raise PolygonNormalError(_in)
        
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
        # type: (list[Polygon]) -> None
        """ Adds new child Poly Id-Numbers to the 'children' list. Used for
        hosted surfaces such as windows and doors.
        
        Arguments:
        ----------
            * _child_polys (list[Polygon]): A list of Poly objects to add as children of the host.
        """
        if not _child_polys: return

        if not isinstance(_child_polys, list):
            _child_polys = [ _child_polys ]
        
        for child_poly in _child_polys:
            if child_poly.id not in self.children:
                self.children.append( child_poly.id )

class Geom(_Base):
    """Geometry Collection"""

    def __init__(self):
        super(Geom, self).__init__()
        self.polygons = []
    
    @property
    def vertices(self):
        return (v for p in self.polygons for v in p.vertices)

    def add_component_polygons( self, _compos):
        # type: (list[Component]) -> None
        """Adds component's polygons to the Geometry's 'polygons' list
        
        Arguments:
        ----------
            * _compos (list[Component]): The components to add the polygons from
        """
        
        if not isinstance(_compos, list):
            _compos = [ _compos ]

        for compo in _compos:
            for poly in compo.polygons:
                if poly not in self.polygons:
                    self.polygons.append( poly )


