# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Occupant Utilization Pattern Classes
"""

import PHX._base

class VentilationUtilization(PHX._base._Base):
    def __init__(self, _dos, _pdf):
        super(VentilationUtilization, self).__init__()
        self.daily_op_sched = _dos
        self.frac_of_design_airflow = _pdf

class UtilizationVentilationPattern(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(UtilizationVentilationPattern, self).__init__()
        self.id = self._count
        self.n = '_default_24hr_operation_schd_'
        self.OperatingDays = 7
        self.OperatingWeeks = 52
        #self.MSBMdf = [ [0, 1], [24, 0.77], [0, 0.54], [0, 0.4] ]

        self.utilizations = {
            'Maximum':  VentilationUtilization( 0, 1.00),
            'Standard': VentilationUtilization(24, 0.77),
            'Basic':    VentilationUtilization( 0, 0.54),
            'Minimum':  VentilationUtilization( 0, 0.40),
        }

        self.Maximum_DOS = 0
        self.Maximum_PDF = 1
        self.Standard_DOS = 24
        self.Standard_PDF = 0.77
        self.Basic_DOS = 0
        self.Basic_PDF = 0.54
        self.Minimum_DOS = 0
        self.Minimum_PDF = 0.4

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(UtilizationVentilationPattern, cls).__new__(cls, *args, **kwargs)