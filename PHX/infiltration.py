# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Occupancy class for BldgSegment level"""


import PHX._base


class Infiltration(PHX._base._Base):
    def __init__(self, _host_bldg_segment):
        super(Infiltration, self).__init__()
        self.annual_avg_airflow = 0.0  # m3/h
        self.host_bldg_segment = _host_bldg_segment

    @property
    def q50(self):
        """Envelope Airtightness - m3/h-m2-envelope"""
        try:
            return self.annual_avg_airflow / self.host_bldg_segment.total_envelope_area
        except ZeroDivisionError:
            return 0

    @property
    def n50(self):
        """Volmetric Airtightness - Air-Changes-per-Hour (ACH)"""
        try:
            return self.annual_avg_airflow / self.host_bldg_segment.total_volume_net
        except ZeroDivisionError:
            return 0
