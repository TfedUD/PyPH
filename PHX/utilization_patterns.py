# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Occupant Utilization Pattern Classes
"""

import PHX._base
import PHX.serialization.from_dict
import PHX.occupancy
import PHX.lighting
import PHX.hvac

# -- Ventilation helpers
class Vent_UtilRate(PHX._base._Base):
    def __init__(self, _dos=0, _pdf=0):
        super(Vent_UtilRate, self).__init__()
        self._daily_op_sched = _dos
        self._frac_of_design_airflow = _pdf

    @property
    def daily_op_sched(self):
        """Hours / Day of operation (0-24)"""
        return self._daily_op_sched

    @daily_op_sched.setter
    def daily_op_sched(self, _in):
        if _in is None:
            return

        try:
            _in = float(_in)
        except ValueError:
            raise ValueError('Error: Input must be a number. Got: "{}", type: "{}"'.format(_in, type(_in)))

        if _in > 24.0:
            raise ValueError('Error: Cannot set hours of operation higher than 24. Got: "{}"'.format(_in))

        self._daily_op_sched = _in

    @property
    def frac_of_design_airflow(self):
        return self._frac_of_design_airflow

    @frac_of_design_airflow.setter
    def frac_of_design_airflow(self, _in):
        if _in is None:
            return

        try:
            _in = float(_in)
        except ValueError:
            raise ValueError('Error: Input must be a number. Got: "{}", type: "{}"'.format(_in, type(_in)))

        if _in > 1.0:
            _in = _in / 100

        self._frac_of_design_airflow = _in

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Vent_UtilRate(cls, _dict)


class Vent_UtilRates(PHX._base._Base):
    def __init__(self):
        super(Vent_UtilRates, self).__init__()
        self.maximum = Vent_UtilRate()
        self.standard = Vent_UtilRate()
        self.basic = Vent_UtilRate()
        self.minimum = Vent_UtilRate()

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Vent_UtilRates(cls, _dict)


# -- Primary Utilization Pattern Objects
class UtilPat_Vent(PHX._base._Base):

    _count = 0
    _default = None

    def __init__(self):
        super(UtilPat_Vent, self).__init__()
        self.id = self._count
        self.name = ""
        self.operating_days = 7
        self.operating_weeks = 52

        self.utilization_rates = Vent_UtilRates()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(UtilPat_Vent, cls).__new__(cls, *args, **kwargs)

    def validate_total_hours(self):
        # type: (UtilPat_Vent) -> None | str
        """
        Return a warning if the Utilization Pattern's total utilization hours do not equal 24

        Returns:
        --------
            * (None | str): If total utilization hours == 24 (hrs), returns None.
                If total does not equal 24 (hrs), returns a warning message.
        """

        TOLERANCE = 0.001

        total_operating_hours = 0
        total_operating_hours += self.utilization_rates.maximum.daily_op_sched
        total_operating_hours += self.utilization_rates.standard.daily_op_sched
        total_operating_hours += self.utilization_rates.basic.daily_op_sched
        total_operating_hours += self.utilization_rates.minimum.daily_op_sched

        if 24.0 - total_operating_hours > TOLERANCE:
            return "Error: total hours input ({}) do not total 24. Please check your inputs.".format(
                total_operating_hours
            )

    @classmethod
    def default(cls):
        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.n = "_default_24hr_operation_schd_"

        new_obj.utilization_rates.maximum.daily_op_sched = 0
        new_obj.utilization_rates.maximum.frac_of_design_airflow = 1.00

        new_obj.utilization_rates.standard.daily_op_sched = 24
        new_obj.utilization_rates.standard.frac_of_design_airflow = 0.77

        new_obj.utilization_rates.basic.daily_op_sched = 0
        new_obj.utilization_rates.basic.frac_of_design_airflow = 0.50

        new_obj.utilization_rates.minimum.daily_op_sched = 0
        new_obj.utilization_rates.minimum.frac_of_design_airflow = 0.34

        cls._default = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._UtilPat_Vent(cls, _dict)


class UtilPat_Occupancy(PHX._base._Base):

    _count = 0
    _default = None

    def __init__(self):
        self.id = self._count
        super(UtilPat_Occupancy, self).__init__()
        self.start_hour = 0
        self.end_hour = 1
        self.annual_utilization_days = 0
        self.annual_utilization_factor = 0.0

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._UtilPat_Occupancy(cls, _dict)

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(UtilPat_Occupancy, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls):
        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.start_hour = 1
        new_obj.end_hour = 24
        new_obj.annual_utilization_days = 365
        new_obj.annual_utilization_factor = 1.0

        cls._default = new_obj
        return new_obj

    @property
    def unique_key(self):
        """Return a key uniqu to this 'type' (collection of values) of pattern"""
        return "{}_{}_{}_{}_".format(
            self.start_hour, self.end_hour, self.annual_utilization_days, self.annual_utilization_factor
        )


class UtilPat_Lighting(PHX._base._Base):

    _count = 0
    _default = None

    def __init__(self):
        self.id = self._count
        super(UtilPat_Lighting, self).__init__()
        self.annual_utilization_factor = 1.0

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._UtilPat_Lighting(cls, _dict)

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(UtilPat_Lighting, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls):
        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.annual_utilization_factor = 1.0

        cls._default = new_obj
        return new_obj

    @property
    def unique_key(self):
        """Return a key uniqu to this 'type' (collection of values) of pattern"""
        return "{}_".format(self.annual_utilization_factor)
