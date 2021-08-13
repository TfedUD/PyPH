# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Occupancy class for BldgSegment level"""


import PHX._base


class Infiltration(PHX._base._Base):
    def __init__(self):
        super(Infiltration, self).__init__()
        self.peak_airflow_at_50Pa = 0.0  # - m3/h
        self.annual_reduction_factor = 0.0
        self.total_envelope_area = 0.0  # - m3/h-m2
        self.total_volume = 0.0  # - m3

    @property
    def annual_avg_airflow(self):
        return self.peak_airflow_at_50Pa * self.annual_reduction_factor

    @property
    def q50(self):
        return self.total_airflow_at_50Pa / self.total_envelope_area

    @property
    def n50(self):
        return self.total_airflow_at_50Pa / self.total_volume
