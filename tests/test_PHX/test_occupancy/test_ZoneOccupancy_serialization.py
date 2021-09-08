import PHX.occupancy


def test_ZoneOccupancy_serialization(reset_occupancies):
    o1 = PHX.occupancy.ZoneOccupancy()
    d = o1.to_dict()

    o2 = PHX.occupancy.ZoneOccupancy.from_dict(d)

    assert d == o2.to_dict()
