# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Rhino/Grasshopper functions for manaing BuildingSegment information"""

import uuid


class BldgSegment_ID(object):
    _count = 0

    def __init__(self):
        self.identifier = str(uuid.uuid4())
        self.id = self._count
        self.name = ""

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(BldgSegment_ID, cls).__new__(cls, *args, **kwargs)

    def __eq__(self, other):
        if (
            self.identifier == other.identifier
            and self.id == other.id
            and self.name == other.name
        ):
            return True
        else:
            return False

    def to_dict(self):
        d = {}

        d.update({"identifier": self.identifier})
        d.update({"id": self.id})
        d.update({"name": self.name})
        return d

    @classmethod
    def from_dict(cls, _in):
        o = cls()
        o.identifier = _in.get("identifier")
        o.id = _in.get("id")
        o.name = _in.get("name")
        return o

    def __str__(self):
        return "{}: {}-{}".format(self.__class__.__name__, self.id, self.name)

    def __repr__(self):
        return "{}(id={}, name={})".format(self.__class__.__name__, self.id, self.name)

    def ToString(self):
        return str(self)
