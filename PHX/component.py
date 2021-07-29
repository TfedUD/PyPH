# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Component Classes
"""

from ._base import _Base

class WP_Color(_Base):

    def __init__(self, _a=255, _r=255, _g=255, _b=255):
        super(WP_Color, self).__init__()
        self.alpha = _a
        self.red = _r
        self.green = _g
        self.blue = _b

class Component(_Base):
    
    _count = 0

    def __init__(self):
        super(Component, self).__init__()
        self.id = self._count
        self.idSKP = self._count
        self.n = ""
        self.visC = True
        self.type = 1
        self.idIC = 1
        self.nmIC = None
        self.idEC = -1
        self.nmEC = None
        self.id_color_int = 5
        self.id_color_ext = 5
        self.ud_colog_int = WP_Color()
        self.ud_colog_ext = WP_Color()
        self.inner_srfc_compo_idNr = -1
        self.polygons = []
        self.idAssC = -1
        self.idWtC = -1
    
    @property
    def polygon_id_list(self):
        """Get the list of the Component's Poly id numbers
        
        Returns:
        --------
            * list[int]: ie: [10000001, 10000002, .... ]
        """

        return [ poly.id for poly in self.polygons ]

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(Component, cls).__new__(cls, *args, **kwargs)
    
    def add_polygons(self, _polygons):
        """Adds a Polygon or list of Polygons to the Component

        Arguments:
        ----------
            * _polygons (list[Polygon]): The Polygons to add to the Component
        
        Returns:
        --------
            * None
        """
        
        if not isinstance( _polygons, list ):
            _polygons = [ _polygons ]
        
        for p in _polygons:
            self.polygons.append( p )   

    def add_window_as_child(self, _window_component, _poly_identifier ): #-> None
        """Adds a Window's Polygons as 'children' of the Component's Polygon

        Arguments:
        ----------
            * _window_component (Component): The Window Component to add as a child
            * _poly_identifier (str): The identifier of the polygon face to add the Window to
        """
        
        for p in self.polygons:
            if p.identifier == _poly_identifier:
                p.add_children( _window_component.polygons )