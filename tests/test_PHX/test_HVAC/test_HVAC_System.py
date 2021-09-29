import PHX.hvac_system
import PHX.hvac_components
import PHX.bldg_segment
import PHX.spaces
import PHX.programs.ventilation
import PHX.hvac_components
import pytest


def test_hvac_zone_coverage(reset_hvac):
    d1 = PHX.hvac_system.HVAC_System_ZoneCover()
    d2 = PHX.hvac_system.HVAC_System_ZoneCover()

    assert d1 and d2
    assert d1 != d2


def test_hvac_system(reset_hvac):
    s1 = PHX.hvac_system.HVAC_System()
    s2 = PHX.hvac_system.HVAC_System()

    assert s1 and s2
    assert s1 != s2
    assert s1.id != s2.id


def test_add_devices_to_system(reset_hvac):
    d1 = PHX.hvac_components.HVAC_Device()
    d2 = PHX.hvac_components.HVAC_Device()
    d3 = PHX.hvac_components.HVAC_Device()

    s1 = PHX.hvac_system.HVAC_System()

    s1.add_devices_to_system(d1)
    assert len(s1.devices) == 1
    assert d1 in s1.devices

    s1.add_devices_to_system([d2, d3])
    assert len(s1.devices) == 3
    assert d2 in s1.devices
    assert d3 in s1.devices

    # verfiy no duplicates
    s1.add_devices_to_system(d1)
    assert len(s1.devices) == 3


def test_add_not_devices_to_system(reset_hvac):
    s1 = PHX.hvac_system.HVAC_System()

    with pytest.raises(PHX.hvac_system.HVACSystemAddError):
        s1.add_devices_to_system("Not a Device")

    assert len(s1.devices) == 0


def test_add_zone_to_coverage(reset_hvac):
    s1 = PHX.hvac_system.HVAC_System()
    z1 = PHX.bldg_segment.Zone()

    s1.add_zone_to_system_coverage(z1)
    zone_ids_covered = {_.idZoneCovered for _ in s1.lZoneCover}
    assert z1.id in zone_ids_covered
