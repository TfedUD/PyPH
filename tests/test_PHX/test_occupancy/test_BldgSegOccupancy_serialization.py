import PHX.occupancy


def test_ZoneOccupancy_serialization(reset_occupancies):
    o1 = PHX.occupancy.BldgSegmentOccupancy()
    d = o1.to_dict()

    o2 = PHX.occupancy.BldgSegmentOccupancy.from_dict(d)

    assert d == o2.to_dict()
