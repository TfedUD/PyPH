import PHX.occupancy


def test_SpaceOccupancy(reset_occupancies):
    o1 = PHX.occupancy.SpaceOccupancy()
    o2 = PHX.occupancy.SpaceOccupancy()

    assert o1.id != o2.id


def test_default_SpaceOccupancy(reset_occupancies):
    o1 = PHX.occupancy.SpaceOccupancy.default()
    o2 = PHX.occupancy.SpaceOccupancy.default()

    assert o1.id == o2.id


def test_SpaceOccupancy_unique_key(reset_occupancies):
    o1 = PHX.occupancy.SpaceOccupancy()
    o2 = PHX.occupancy.SpaceOccupancy()

    assert o1.unique_key == o2.unique_key

    o1.name = "this"
    o2.name = "that"
    o1.people_per_area = 1
    o2.people_per_area = 1
    o1.utilization = PHX.utilization_patterns.UtilPat_Occupancy()
    o2.utilization = PHX.utilization_patterns.UtilPat_Occupancy()
    assert o1.unique_key != o2.unique_key

    o1.name = ""
    o2.name = ""
    o1.people_per_area = 1
    o2.people_per_area = 2
    o1.utilization = PHX.utilization_patterns.UtilPat_Occupancy()
    o2.utilization = PHX.utilization_patterns.UtilPat_Occupancy()
    assert o1.unique_key != o2.unique_key

    o1.name = ""
    o2.name = ""
    o1.people_per_area = 1
    o2.people_per_area = 1
    o1.utilization = PHX.utilization_patterns.UtilPat_Occupancy()
    o1.utilization.start_hour = 1
    o2.utilization = PHX.utilization_patterns.UtilPat_Occupancy()
    o1.utilization.start_hour = 2
    assert o1.unique_key != o2.unique_key
