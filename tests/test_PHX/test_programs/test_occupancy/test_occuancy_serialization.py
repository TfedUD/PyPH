import PHX.programs.occupancy


def test_BldgSegmentOccupancy_serialization(reset_occupancies):
    o1 = PHX.programs.occupancy.BldgSegmentOccupancy()
    d = o1.to_dict()

    o2 = PHX.programs.occupancy.BldgSegmentOccupancy.from_dict(d)

    assert d == o2.to_dict()


def test_SpaceOccupancy_serialization(reset_occupancies):
    o1 = PHX.programs.occupancy.SpaceOccupancy()
    d = o1.to_dict()

    o2 = PHX.programs.occupancy.SpaceOccupancy.from_dict(d)

    assert d == o2.to_dict()


def test_ZoneOccupancy_serialization(reset_occupancies):
    o1 = PHX.programs.occupancy.ZoneOccupancy()
    d = o1.to_dict()

    o2 = PHX.programs.occupancy.ZoneOccupancy.from_dict(d)

    assert d == o2.to_dict()
