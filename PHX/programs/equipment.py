# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Program: Equipment Class
"""

import PHX._base


class EquipmentSet(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(EquipmentSet, self).__init__()
        self.id = self._count
        self.ventilator = None

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(EquipmentSet, cls).__new__(cls, *args, **kwargs)
