"""Collections / Organizations of data in WUFI-specific format"""


class UtilizationPattern_NonRes:

    _count = 0

    def __init__(self):
        self._id = self._count
        self.occupancy = None
        self.lighting = None

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(UtilizationPattern_NonRes, cls).__new__(cls, *args, **kwargs)


class UtilizationPattern_Vent:

    _count = 0

    def __init__(self):
        self.id = self._count

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(UtilizationPattern_Vent, cls).__new__(cls, *args, **kwargs)
