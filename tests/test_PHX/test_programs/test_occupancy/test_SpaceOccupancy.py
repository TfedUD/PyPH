import PHX.occupancy
import PHX.loads
import PHX.schedules


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
    o1.loads.people_per_area = 1
    o2.loads.people_per_area = 1
    o1.schedule = PHX.schedules.Schedule_Occupancy()
    o2.schedule = PHX.schedules.Schedule_Occupancy()
    assert o1.unique_key != o2.unique_key

    o1.name = ""
    o2.name = ""
    o1.loads.people_per_area = 1
    o2.loads.people_per_area = 2
    o1.schedule = PHX.schedules.Schedule_Occupancy()
    o2.schedule = PHX.schedules.Schedule_Occupancy()
    assert o1.unique_key != o2.unique_key

    o1.name = ""
    o2.name = ""
    o1.loads.people_per_area = 1
    o2.loads.people_per_area = 1
    o1.schedule = PHX.schedules.Schedule_Occupancy()
    o1.schedule.start_hour = 1
    o2.schedule = PHX.schedules.Schedule_Occupancy()
    o1.schedule.start_hour = 2
    assert o1.unique_key != o2.unique_key
