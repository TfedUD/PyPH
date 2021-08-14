# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for handlding boundary-condition / exposure related issues"""

import honeybee.room


def is_PHIUS_exposed(_hb_face):
    # type: (honeybee.face.Face) -> bool
    """Is the Honeybee Face a PHIUS 'Exposed Surface' for q50 calculations?

    Note: for q50 values: PHIUS exterior 'exposed surfaces' includes the ground, while
    the normal Honeybee "room.exposed_area" property does NOT.
    """

    if "ADIABATIC" in str(_hb_face.boundary_condition).upper():
        return False
    elif "SURFACE" in str(_hb_face.boundary_condition).upper():
        return False
    else:
        # includes: Ground, Outdoors
        return True


def hb_room_PHX_exposed_area(_hb_room):
    # type: (honeybee.room.Room) -> float
    """Returns Honeybee room's total expose area (m2) including ground (as per PHIUS)"""

    return sum(float(face.area) for face in _hb_room.faces if is_PHIUS_exposed(face))
