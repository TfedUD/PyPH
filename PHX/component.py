# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Component Classes
"""

import PHX._base
import PHX.geometry


class ComponentTypeError(Exception):
    def __init__(self, _in):
        self.message = 'Error: Expected input of type: "PHX.component.Component" Got: "{}"::"{}"?'.format(
            _in, type(_in)
        )
        super(ComponentTypeError, self).__init__(self.message)


class WindowHostNotFoundError(Exception):
    def __init__(self, _p, _c):
        self.message = 'Error: No window host polygon with ID: "{}" found on Component: "{}"'.format(_p.id, _c.name)
        super(WindowHostNotFoundError, self).__init__(self.message)


class WP_Color(PHX._base._Base):
    def __init__(self, _a=255, _r=255, _g=255, _b=255):
        super(WP_Color, self).__init__()
        self.alpha = _a
        self.red = _r
        self.green = _g
        self.blue = _b


class Component(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(Component, self).__init__()
        self.id = self._count
        self.idSKP = self._count
        self.name = "No Name"
        self.visC = True
        self.type = 1
        self.int_exposure_zone_id = 1
        self.int_exposure_zone_name = None
        self.ext_exposure_zone_id = -1
        self.ext_exposure_zone_name = None
        self.int_color_id = 5
        self.ext_color_id = 5
        self.int_UD_color = WP_Color()
        self.ext_UD_color = WP_Color()
        self.inner_srfc_compo_idNr = -1
        self.polygons = []
        self.assembly_id_num = -1
        self.win_type_id_num = -1

    @property
    def exposed_area(self):
        # Note: Excludes windows and door area, since that would double count
        # Opaque areas are not 'punched' areas (yet).
        if self.type != 1:
            return 0  # Only include Opaque surfaces
        if self.ext_exposure_zone_id not in [-1, -2]:
            return 0  # Exclude Adiabatic / Surface Expsure

        return sum(_.area for _ in self.polygons)

    @property
    def polygon_id_list(self):
        """Get the list of the Component's Poly id numbers

        Returns:
        --------
            * list[int]: ie: [10000001, 10000002, .... ]
        """

        return [poly.id for poly in self.polygons]

    def set_host_zone_name(self, _zone):
        self.int_exposure_zone_id = _zone.id
        self.int_exposure_zone_name = "Zone {}: {}".format(_zone.id, _zone.name)

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Component, cls).__new__(cls, *args, **kwargs)

    def __add__(self, _other):
        self.polygons.extend(_other.polygons)
        return self

    __radd__ = __add__

    def add_polygons(self, _polygons):
        # type: (list[PHX.geometry.Polygon]) -> None
        """Adds a Polygon or list of Polygons to the Component

        Arguments:
        ----------
            * _polygons (list[Polygon]): The Polygons to add to the Component
        """

        if not isinstance(_polygons, list):
            _polygons = [_polygons]

        for p in _polygons:
            if not isinstance(p, PHX.geometry.Polygon):
                raise PHX.geometry.PolygonTypeError(p)
            if p in self.polygons:
                continue

            self.polygons.append(p)

    def add_window_as_child(self, _window_component, _poly_identifier):
        # type (Component, str) -> None
        """Adds a Window's Polygons as 'children' of a Component's existing Polygon

        Arguments:
        ----------
            * _window_component (Component): The Window Component to add as a child
            * _poly_identifier (str): The identifier of the polygon face to add the Window to
        """

        for p in self.polygons:
            if p.identifier != _poly_identifier:
                continue

            p.add_children(_window_component.polygons)
            break
        else:
            raise WindowHostNotFoundError(p, self)
