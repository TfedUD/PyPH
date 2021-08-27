import PHX.bldg_segment
import PHX.spaces


def test_Zone_identifier(reset_bldg_segment_count):
    z1 = PHX.bldg_segment.Zone()
    z2 = PHX.bldg_segment.Zone()

    assert z1.identifier != z2.identifier


def test_Zone_ID(reset_bldg_segment_count):
    assert PHX.bldg_segment.Zone._count == 0

    z1 = PHX.bldg_segment.Zone()
    assert PHX.bldg_segment.Zone._count == 1

    z2 = PHX.bldg_segment.Zone()
    assert PHX.bldg_segment.Zone._count == 2


def test_add_new_Space():
    z1 = PHX.bldg_segment.Zone()
    r1 = PHX.spaces.Space()

    assert len(z1.spaces) == 0
    z1.add_spaces(r1)
    assert r1 in z1.spaces
    assert len(z1.spaces) == 1
