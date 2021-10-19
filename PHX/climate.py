# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Climate / Weather PHX Classes"""

import PHX._base
import PHX.serialization.from_dict


class Climate_MonthlyValueCollection(PHX._base._Base):
    """Collection class to organize monthly cliamte values"""

    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    def __init__(self):
        super(Climate_MonthlyValueCollection, self).__init__()
        for month in self.months:
            setattr(self, month, 0)

    @property
    def values(self):
        return [getattr(self, month) for month in self.months]

    @values.setter
    def values(self, _in):
        if (_in is None) or (len(_in) != 12):
            return

        for i, month in enumerate(self.months):
            setattr(self, month, _in[i])

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Climate_MonthlyValueCollection(cls, _dict)


class Climate_PeakLoadCollection(PHX._base._Base):
    """Collection class to orgaize peak load weather data"""

    def __init__(self):
        super(Climate_PeakLoadCollection, self).__init__()
        self.temp = 0
        self.rad_north = 0
        self.rad_east = 0
        self.rad_south = 0
        self.rad_west = 0
        self.rad_global = 0

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Climate_PeakLoadCollection(cls, _dict)


class Climate_Location(PHX._base._Base):
    def __init__(self):
        super(Climate_Location, self).__init__()
        # NYC Default
        self.latitude = 40.6
        self.longitude = -73.8
        self.weather_station_elevation = 3.0
        self.climate_zone = 1
        self.hours_from_UTC = -4

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Climate_Location(cls, _dict)


class Climate_Ground(PHX._base._Base):
    def __init__(self):
        super(Climate_Ground, self).__init__()
        self.ground_thermal_conductivity = 2
        self.ground_heat_capacitiy = 1000
        self.ground_density = 2000
        self.depth_groundwater = 3
        self.flow_rate_groundwater = 0.05

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Climate_Ground(cls, _dict)


class Climate(PHX._base._Base):
    def __init__(self):
        super(Climate, self).__init__()
        self.name = None
        self.summer_daily_temperature_swing = 8  # Deg K
        self.average_wind_speed = 4

        self.location = Climate_Location()
        self.ground = Climate_Ground()

        self.monthly_temperature_air = Climate_MonthlyValueCollection()
        self.monthly_temperature_dewpoint = Climate_MonthlyValueCollection()
        self.monthly_temperature_sky = Climate_MonthlyValueCollection()
        self.monthly_temperature_ground = Climate_MonthlyValueCollection()

        self.monthly_radiation_north = Climate_MonthlyValueCollection()
        self.monthly_radiation_east = Climate_MonthlyValueCollection()
        self.monthly_radiation_south = Climate_MonthlyValueCollection()
        self.monthly_radiation_west = Climate_MonthlyValueCollection()
        self.monthly_radiation_global = Climate_MonthlyValueCollection()

        self.peak_heating_1 = Climate_PeakLoadCollection()
        self.peak_heating_2 = Climate_PeakLoadCollection()
        self.peak_cooling = Climate_PeakLoadCollection()

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Climate(cls, _dict)
