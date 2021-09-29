import PHX.programs.occupancy


def test_occupancy(reset_occupancies):
    o1 = PHX.programs.occupancy.BldgSegmentOccupancy()
    o2 = PHX.programs.occupancy.BldgSegmentOccupancy()

    assert o1.id != o2.id


def test_occupancy_equal(reset_occupancies):
    zo1 = PHX.programs.occupancy.BldgSegmentOccupancy()
    zo1.category = 1
    zo1.usage_type = 1
    zo1.num_units = 1
    zo1.num_stories = 1

    zo2 = PHX.programs.occupancy.BldgSegmentOccupancy()
    zo2.category = 1
    zo2.usage_type = 1
    zo2.num_units = 1
    zo2.num_stories = 1

    assert zo1 == zo2


def test_occupancy_not_equal(reset_occupancies):
    zo1 = PHX.programs.occupancy.BldgSegmentOccupancy()
    zo2 = PHX.programs.occupancy.BldgSegmentOccupancy()

    zo1.category = 1
    zo2.category = 1
    zo1.usage_type = 1
    zo2.usage_type = 1
    zo1.num_units = 1
    zo2.num_units = 1
    zo1.num_stories = 1
    zo2.num_stories = 1
    assert zo1 == zo2

    zo1.category = 1
    zo2.category = 2  # <----
    zo1.usage_type = 1
    zo2.usage_type = 1
    zo1.num_units = 1
    zo2.num_units = 1
    zo1.num_stories = 1
    zo2.num_stories = 1
    assert zo1 != zo2

    zo1.category = 1
    zo2.category = 1
    zo1.usage_type = 1
    zo2.usage_type = 2  # <----
    zo1.num_units = 1
    zo2.num_units = 1
    zo1.num_stories = 1
    zo2.num_stories = 1
    assert zo1 != zo2

    zo1.category = 1
    zo2.category = 1
    zo1.usage_type = 1
    zo2.usage_type = 1
    zo1.num_units = 1
    zo2.num_units = 2  # <----
    zo1.num_stories = 1
    zo2.num_stories = 1
    assert zo1 != zo2

    zo1.category = 1
    zo2.category = 1
    zo1.usage_type = 1
    zo2.usage_type = 1
    zo1.num_units = 1
    zo2.num_units = 1
    zo1.num_stories = 1
    zo2.num_stories = 2  # <----
    assert zo1 != zo2


def test_occupancy_validation():
    o1 = PHX.programs.occupancy.BldgSegmentOccupancy()

    # -- Res Types
    # good combo, no error returned
    o1.category = 1
    o1.usage_type = 1
    assert not o1.validate()

    # Bad combo, return an error
    o1.category = 1
    o1.usage_type = 4
    assert o1.validate()

    # -- Non-Res Types
    # good combo, no error returned
    o1.category = 2
    o1.usage_type = 4
    assert not o1.validate()

    # good combo, no error returned
    o1.category = 2
    o1.usage_type = 5
    assert not o1.validate()

    # good combo, no error returned
    o1.category = 2
    o1.usage_type = 6
    assert not o1.validate()

    # good combo, no error returned
    o1.category = 2
    o1.usage_type = 7
    assert not o1.validate()

    # Bad combo, return an error
    o1.category = 2
    o1.usage_type = 1
    assert o1.validate()

    # Bad combo, return an error
    o1.category = 3
    assert o1.validate()
