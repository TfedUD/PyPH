# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Occupant Utilization Pattern Classes
"""

import PHX._base
import PHX.serialization.from_dict


class VentilationUtilization(PHX._base._Base):
    def __init__(self, _dos=0, _pdf=0):
        super(VentilationUtilization, self).__init__()
        self._daily_op_sched = _dos
        self._frac_of_design_airflow = _pdf

    @property
    def daily_op_sched(self):
        return self._daily_op_sched

    @daily_op_sched.setter
    def daily_op_sched(self, _in):
        if _in is None:
            return

        try:
            _in = float(_in)
        except ValueError:
            raise ValueError(
                'Error: Input must be a number. Got: "{}", type: "{}"'.format(
                    _in, type(_in)
                )
            )

        if _in > 24.0:
            raise ValueError(
                'Error: Cannot set hours of operation higher than 24. Got: "{}"'.format(
                    _in
                )
            )

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
            raise ValueError(
                'Error: Input must be a number. Got: "{}", type: "{}"'.format(
                    _in, type(_in)
                )
            )

        if _in > 1.0:
            _in = _in / 100

        self._frac_of_design_airflow = _in

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._VentilationUtilization(cls, _dict)


class VentilationUtilizations(PHX._base._Base):
    def __init__(self):
        super(VentilationUtilizations, self).__init__()
        self.maximum = VentilationUtilization()
        self.standard = VentilationUtilization()
        self.basic = VentilationUtilization()
        self.minimum = VentilationUtilization()

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._VentilationUtilizations(cls, _dict)


class UtilizationPattern_Ventilation(PHX._base._Base):

    _count = 0
    _default = None

    def __init__(self):
        super(UtilizationPattern_Ventilation, self).__init__()
        self.id = self._count
        self.n = ""
        self.OperatingDays = 7
        self.OperatingWeeks = 52

        self.utilizations = VentilationUtilizations()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(UtilizationPattern_Ventilation, cls).__new__(cls, *args, **kwargs)

    def validate_total_hours(self):

        total_operating_hours = 0
        total_operating_hours += self.utilizations.maximum.daily_op_sched
        total_operating_hours += self.utilizations.standard.daily_op_sched
        total_operating_hours += self.utilizations.basic.daily_op_sched
        total_operating_hours += self.utilizations.minimum.daily_op_sched

        if total_operating_hours != 24.0:
            return "Error: hours do not total 24. Please check your inputs."

    @classmethod
    def default(cls):
        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.n = "_default_24hr_operation_schd_"

        new_obj.utilizations.maximum.daily_op_sched = 0
        new_obj.utilizations.maximum.frac_of_design_airflow = 1.00

        new_obj.utilizations.standard.daily_op_sched = 24
        new_obj.utilizations.standard.frac_of_design_airflow = 0.77

        new_obj.utilizations.basic.daily_op_sched = 0
        new_obj.utilizations.basic.frac_of_design_airflow = 0.50

        new_obj.utilizations.minimum.daily_op_sched = 0
        new_obj.utilizations.minimum.frac_of_design_airflow = 0.34

        cls._default = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._UtilizationPattern_Ventilation(cls, _dict)
