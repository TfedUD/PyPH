# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Occupant Utilization Pattern Classes
"""

import PHX._base

class VentilationUtilization(PHX._base._Base):
    def __init__(self, _dos=0, _pdf=0):
        super(VentilationUtilization, self).__init__()
        self.daily_op_sched = _dos
        self.frac_of_design_airflow = _pdf

    def set(self, _op_sched, _frac_of_des_air):
        self.daily_op_sched = _op_sched
        self.frac_of_design_airflow = _frac_of_des_air

class VentilationUtilizations(PHX._base._Base):
    
    def __init__(self):
        super(VentilationUtilizations, self).__init__()
        self.maximum = VentilationUtilization()
        self.standard = VentilationUtilization()
        self.basic = VentilationUtilization()
        self.minimum = VentilationUtilization()

class UtilizationPattern_Ventilation(PHX._base._Base):

    _count = 0
    _default = None

    def __init__(self):
        super(UtilizationPattern_Ventilation, self).__init__()
        self.id = self._count
        self.n = ''
        self.OperatingDays = 7
        self.OperatingWeeks = 52

        self.utilizations = VentilationUtilizations()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(UtilizationPattern_Ventilation, cls).__new__(cls, *args, **kwargs)
    
    @classmethod
    def default(cls):
        if cls._default: return cls._default
        
        new_obj = cls()
        new_obj.n = '_default_24hr_operation_schd_'
        new_obj.utilizations.maximum.set( 0, 1.00 )
        new_obj.utilizations.standard.set(24, 0.77 )
        new_obj.utilizations.basic.set( 0, 1.00 )
        new_obj.utilizations.minimum.set( 0, 1.00 )

        cls._default = new_obj
        return new_obj


    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._UtilizationVentilationPattern(cls, _dict)
