import PHX.variant
import PHX.spaces

def test_Zone_identifier(reset_variant_count):
    z1 = PHX.variant.Zone()
    z2 = PHX.variant.Zone()

    assert z1.identifier != z2.identifier

    z1.n = "My Name"
    assert z1.wp_display_name == 'Zone 1: My Name'

def test_Zone_ID(reset_variant_count):
    assert PHX.variant.Zone._count == 0

    z1 = PHX.variant.Zone()
    assert PHX.variant.Zone._count == 1

    z2 = PHX.variant.Zone()
    assert PHX.variant.Zone._count == 2

def test_add_new_Space():
    z1 = PHX.variant.Zone()
    r1 = PHX.spaces.Space()

    assert len(z1.rooms_ventilation) == 0
    z1.add_new_space( r1 )
    assert r1 in z1.rooms_ventilation
    assert len(z1.rooms_ventilation) == 1

