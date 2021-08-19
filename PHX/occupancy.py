# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Occupancy class for BldgSegment level"""


import PHX._base


class ZoneOccupancy(PHX._base._Base):
    _count = 0

    def __init__(self):
        self.id = self._count
        super(ZoneOccupancy, self).__init__()
        self.num_occupants = 0
        self.num_bedrooms = 0
        self.num_dwelling_units = 0

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(ZoneOccupancy, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._ZoneOccupancy(cls, _dict)

    def __eq__(self, other):
        # type: (ZoneOccupancy, ZoneOccupancy) -> bool
        if (
            self.num_occupants != other.num_occupants
            or self.num_bedrooms != other.num_bedrooms
            or self.num_dwelling_units != other.num_dwelling_units
        ):
            return False
        else:
            return True

    def __add__(self, other):
        # type: (ZoneOccupancy, ZoneOccupancy) -> ZoneOccupancy
        self.num_occupants = int(self.num_occupants) + int(other.num_occupants)
        self.num_bedrooms = int(self.num_bedrooms) + int(other.num_bedrooms)
        self.num_dwelling_units = int(self.num_dwelling_units) + int(other.num_dwelling_units)

        return self


class BldgSegmentOccupancy(PHX._base._Base):
    _count = 0

    def __init__(self):
        self.id = self._count
        super(BldgSegmentOccupancy, self).__init__()
        self.category = 1
        self.usage_type = 1
        self.num_units = 1
        self.num_stories = 1

    def validate(self):
        """Ensure all values are allowed / compatible"""
        if self.category == 1:
            if self.usage_type == 1:
                return None
            else:
                return 'Error: Usage-Type of "{}" not allowed with Occupancy-Category "{}".'.format(
                    self.usage_type, self.category
                )
        elif self.category == 2:
            if self.usage_type in [4, 5, 6, 7]:
                return None
            else:
                return 'Error: Usage-Type of "{}" not allowed with Occupancy-Category "{}".'.format(
                    self.usage_type, self.category
                )
        else:
            return 'Error: Category of "{}" not allowed.'.format(self.category)

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(BldgSegmentOccupancy, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._BldgSegmentOccupancy(cls, _dict)

    def __eq__(self, other):
        # type: (BldgSegmentOccupancy, BldgSegmentOccupancy) -> bool
        if (
            self.category != other.category
            or self.usage_type != other.usage_type
            or self.num_units != other.num_units
            or self.num_stories != other.num_stories
        ):
            return False
        else:
            return True
