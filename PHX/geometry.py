# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Geometry Classes
"""

import PHX._base


class PolygonTypeError(Exception):
    def __init__(self, _in):
        self.message = 'Error: Expected input of type: "PHX.geometry.Polygon" Got: "{}"::"{}"?'.format(
            _in, type(_in)
        )
        super(PolygonTypeError, self).__init__(self.message)


class PolygonNormalError(Exception):
    def __init__(self, _in):
        self.message = (
            'Error: The Polygon "nVec" input should be a Vector with'
            'x,y,z attributes. Instead, got "{}", type: "{}"'.format(_in, type(_in))
        )
        super(PolygonNormalError, self).__init__(self.message)


class Vector(PHX._base._Base):
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


class Vertex(PHX._base._Base):
    """A single Vertex object with x, y, z positions and an ID number

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
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Vertex, cls).__new__(cls, *args, **kwargs)


class Polygon(PHX._base._Base):
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

    _count = 10000000 - 1

    def __init__(self):
        super(Polygon, self).__init__()
        self.id = self._count
        self._nVec = None
        self.idPolyI = []
        self.vertices = []
        self.children = []  # IdentNr of the children

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
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
        if not hasattr(_in, "x") or not hasattr(_in, "y") or not hasattr(_in, "z"):
            raise PolygonNormalError(_in)

        self._nVec = _in

    @property
    def idVert(self):
        """
        Returns:
        --------
            * list[int]: A list of the Polygon's Vertex ID numbers
        """
        return [vert.id for vert in self.vertices]

    def add_children(self, _child_polys):
        # type: (list[Polygon]) -> None
        """Adds new child Poly Id-Numbers to the 'children' list. Used for
        hosted surfaces such as windows and doors.

        Arguments:
        ----------
            * _child_polys (list[Polygon]): A list of Poly objects to add as children of the host.
        """
        if not _child_polys:
            return

        if not isinstance(_child_polys, list):
            _child_polys = [_child_polys]

        for child_poly in _child_polys:
            if not isinstance(child_poly, Polygon):
                raise PolygonTypeError(child_poly)
            if child_poly.id in self.children:
                continue

            self.children.append(child_poly.id)
