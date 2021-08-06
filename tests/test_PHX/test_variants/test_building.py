import PHX.variant
import PHX.component
import pytest


def test_building_identifier():
    b1 = PHX.variant.Building()
    b2 = PHX.variant.Building()

    assert b1.identifier != b2.identifier


def test_add_zone():
    b1 = PHX.variant.Building()
    z1 = PHX.variant.Zone()
    z2 = PHX.variant.Zone()
    z3 = PHX.variant.Zone()

    assert len(b1.lZone) == 0
    b1.add_zones(z1)
    assert z1 in b1.lZone

    b1.add_zones([z2, z3])
    assert z2 in b1.lZone
    assert z3 in b1.lZone
    assert len(b1.lZone) == 3

    # add same one again. Should ignore it
    b1.add_zones(z2)
    assert len(b1.lZone) == 3

    # Try adding not a Zone
    z4 = "I am Not a Zone"
    with pytest.raises(PHX.variant.ZoneTypeError):
        b1.add_zones(z4)


def test_add_components():
    b1 = PHX.variant.Building()
    c1 = PHX.component.Component()
    c2 = PHX.component.Component()
    c3 = PHX.component.Component()

    # Try adding a single one
    b1.add_components(c1)
    assert c1 in b1.lComponent

    # Try adding multiple
    b1.add_components([c2, c3])
    assert c1 in b1.lComponent
    assert c3 in b1.lComponent
    assert c3 in b1.lComponent

    # Try adding the same one again. Should ignore
    assert len(b1.lComponent) == 3
    b1.add_components(c1)
    assert len(b1.lComponent) == 3

    # Try adding not a Component
    c4 = "I am Not a Component"
    with pytest.raises(PHX.component.ComponentTypeError):
        b1.add_components(c4)


def test_get_zone_by_identifier():
    b1 = PHX.variant.Building()
    z1 = PHX.variant.Zone()
    z2 = PHX.variant.Zone()
    z3 = PHX.variant.Zone()

    b1.add_zones([z1, z2, z3])

    got_zone = b1.get_zone_by_identifier(z1.identifier)
    assert got_zone == z1
    assert z1 in b1.lZone

    got_zone = b1.get_zone_by_identifier("Not One I know")
    assert not got_zone
