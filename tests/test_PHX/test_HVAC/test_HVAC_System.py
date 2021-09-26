import PHX.hvac
import PHX.bldg_segment
import PHX.spaces
import PHX.programs.ventilation
import PHX.ventilation_components
import pytest


def test_hvac_zone_coverage(reset_hvac):
    d1 = PHX.hvac.HVAC_System_ZoneCover()
    d2 = PHX.hvac.HVAC_System_ZoneCover()

    assert d1 and d2
    assert d1 != d2


def test_hvac_system(reset_hvac):
    s1 = PHX.hvac.HVAC_System()
    s2 = PHX.hvac.HVAC_System()

    assert s1 and s2
    assert s1 != s2
    assert s1.id != s2.id


def test_add_devices_to_system(reset_hvac):
    d1 = PHX.hvac.HVAC_Device()
    d2 = PHX.hvac.HVAC_Device()
    d3 = PHX.hvac.HVAC_Device()

    s1 = PHX.hvac.HVAC_System()

    s1.add_devices_to_system(d1)
    assert len(s1.lDevice) == 1
    assert d1 in s1.lDevice

    s1.add_devices_to_system([d2, d3])
    assert len(s1.lDevice) == 3
    assert d2 in s1.lDevice
    assert d3 in s1.lDevice

    # verfiy no duplicates
    s1.add_devices_to_system(d1)
    assert len(s1.lDevice) == 3


def test_add_not_devices_to_system(reset_hvac):
    s1 = PHX.hvac.HVAC_System()

    with pytest.raises(PHX.hvac.HVACSystemAddError):
        s1.add_devices_to_system("Not a Device")

    assert len(s1.lDevice) == 0


def test_add_zone_to_coverage(reset_hvac):
    s1 = PHX.hvac.HVAC_System()
    z1 = PHX.bldg_segment.Zone()

    s1.add_zone_to_system_coverage(z1)
    zone_ids_covered = {_.idZoneCovered for _ in s1.lZoneCover}
    assert z1.id in zone_ids_covered


def test_add_zone_with_no_ventilator_to_system(reset_hvac):
    s1 = PHX.hvac.HVAC_System()
    z1 = PHX.bldg_segment.Zone()

    # Add a Zone with no ventilators, and no spaces
    s1.add_zone_ventilators_to_system(z1)
    assert len(s1.lDevice) == 0


def test_add_zone_with_ventilator_to_system(reset_hvac):
    # -- Build the new Ventilation Components, Systems
    new_ventilator = PHX.ventilation_components.Ventilator()

    new_system = PHX.ventilation_components.Ventilation_System()
    new_system.ventilator = new_ventilator

    new_space_vent = PHX.programs.ventilation.SpaceVentilation()
    new_space_vent.system = new_system

    # -- Build the space, add the ventilation systme with the Ventilator
    sp1 = PHX.spaces.Space()
    sp1.ventilation = new_space_vent

    # -- Build the zone, add the space to the Zone
    z1 = PHX.bldg_segment.Zone()
    z1.add_spaces(sp1)

    # -- Build the HVAC System, add the zone's ventilator
    s1 = PHX.hvac.HVAC_System()
    s1.add_zone_ventilators_to_system(z1)
    assert len(s1.lDevice) == 1
    assert new_ventilator in s1.lDevice
