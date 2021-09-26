"""Collections / Organizations of data in WUFI-specific format"""
import PHX.programs.schedules


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
        self.name = None
        self.operating_days = None
        self.operating_weeks = None
        self.utilization_rates = PHX.programs.schedules.Vent_UtilRates()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(UtilizationPattern_Vent, cls).__new__(cls, *args, **kwargs)
