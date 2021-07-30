import PHX.variant

def  test_building_identifier():
    b1 = PHX.variant.Building()
    b2 = PHX.variant.Building()

    assert b1.identifier != b2.identifier

def test_add_zone():
    b1 = PHX.variant.Building()
    z1 = PHX.variant.Zone()
    z2 = PHX.variant.Zone()
    z3 = PHX.variant.Zone()

    assert len(b1.lZone) == 0
    b1.add_zones( z1 )
    assert z1 in b1.lZone

    b1.add_zones( [z2, z3] )
    assert z2 in b1.lZone
    assert z3 in b1.lZone
    assert len(b1.lZone) == 3

    # add same one again. Should ignore
    b1.add_zones( z2 )
    assert len(b1.lZone) == 3
