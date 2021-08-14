# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Occupancy class for BldgSegment level"""


import PHX._base


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
        if (
            self.category != other.category
            or self.usage_type != other.usage_type
            or self.num_units != other.num_units
            or self.num_stories != other.num_stories
        ):
            return False
        else:
            return True
