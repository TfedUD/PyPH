import PHX.programs.occupancy


def test_ZoneOccupancy_count(reset_occupancies):
    zo1 = PHX.programs.occupancy.ZoneOccupancy()
    zo2 = PHX.programs.occupancy.ZoneOccupancy()

    assert zo1.id != zo2.id


def test_ZoneOccupancy_equal(reset_occupancies):
    zo1 = PHX.programs.occupancy.ZoneOccupancy()
    zo1.num_occupants = 12
    zo1.num_bedrooms = 157
    zo1.num_dwelling_units = 345

    zo2 = PHX.programs.occupancy.ZoneOccupancy()
    zo2.num_occupants = 12
    zo2.num_bedrooms = 157
    zo2.num_dwelling_units = 345

    assert zo1 == zo2


def test_ZoneOccupancy_unequal(reset_occupancies):
    zo1 = PHX.programs.occupancy.ZoneOccupancy()
    zo2 = PHX.programs.occupancy.ZoneOccupancy()

    assert zo1 == zo2

    zo1.num_occupants = 12
    zo2.num_occupants = 13  # <---
    zo1.num_bedrooms = 157
    zo2.num_bedrooms = 157
    zo1.num_dwelling_units = 345
    zo2.num_dwelling_units = 345
    assert zo1 != zo2

    zo1.num_occupants = 12
    zo2.num_occupants = 12
    zo1.num_bedrooms = 157
    zo2.num_bedrooms = 158  # <---
    zo1.num_dwelling_units = 345
    zo2.num_dwelling_units = 345
    assert zo1 != zo2

    zo1.num_occupants = 12
    zo2.num_occupants = 12
    zo1.num_bedrooms = 157
    zo2.num_bedrooms = 157
    zo1.num_dwelling_units = 345
    zo2.num_dwelling_units = 346  # <---
    assert zo1 != zo2


def test_ZoneOccupancy_add(reset_occupancies):
    zo1 = PHX.programs.occupancy.ZoneOccupancy()
    zo2 = PHX.programs.occupancy.ZoneOccupancy()

    zo1.num_occupants = 12
    zo2.num_occupants = 13
    zo1.num_bedrooms = 8
    zo2.num_bedrooms = 17
    zo1.num_dwelling_units = 6
    zo2.num_dwelling_units = 19

    zo3 = zo1 + zo2
    assert zo3.num_occupants == 25
    assert zo3.num_bedrooms == 25
    assert zo3.num_dwelling_units == 25
