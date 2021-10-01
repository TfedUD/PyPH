# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Basic HVAC-System Classes
"""

from collections import defaultdict
import PHX._base
import PHX.hvac_components


class HVACSystemAddError(Exception):
    def __init__(self, _in):
        self.message = (
            "Error: Cannot add Device {}, type: {}"
            "to the HVAC System list. Please add only HVAC Devices.".format(_in, type(_in))
        )
        super(HVACSystemAddError, self).__init__(self.message)


class HVAC_System_ZoneCover(PHX._base._Base):
    def __init__(self):
        super(HVAC_System_ZoneCover, self).__init__()
        self.idZoneCovered = 1
        self.cover_heating = 0
        self.cover_cooling = 0
        self.cover_ventilation = 0
        self.cover_humidification = 0
        self.cover_dehumidification = 0


class HVAC_System(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(HVAC_System, self).__init__()
        self.n = ""
        self.typeSys = 1
        self.id = self._count
        self.lZoneCover = []
        self._device_dict = defaultdict(list)
        self.distrib = None
        self.suppDev = None
        self.PHdistrib = None

    @property
    def devices(self):
        return list(self._device_dict.values())

    def add_devices_to_system(self, _devices):
        # type: (list[PHX.hvac_components.HVAC_Device]) -> None
        """Adds any HVAC Devices to the HVAC System"""

        if not isinstance(_devices, list):
            _devices = [_devices]

        for d in _devices:
            if not isinstance(d, PHX.hvac_components.HVAC_Device):
                raise HVACSystemAddError(d)

            # -- Ensure no duplicates
            self._device_dict[d.identifier] = d

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""

        cls._count += 1
        return super(HVAC_System, cls).__new__(cls, *args, **kwargs)

    def add_zone_to_system_coverage(self, _zone):
        # type: (PHX.bldg_segment.Zone) -> None
        """Adds a Zone's id number to the HVAC System's Covered Zones list"""

        new_coverage = HVAC_System_ZoneCover()
        new_coverage.idZoneCovered = _zone.id

        self.lZoneCover.append(new_coverage)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_System(cls, _dict)
