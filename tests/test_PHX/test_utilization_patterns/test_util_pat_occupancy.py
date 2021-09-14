import PHX.schedules


def test_util_pat(reset_util_pattern):
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_2 = PHX.schedules.Schedule_Occupancy()

    assert pattern_1.id == 1
    assert pattern_2.id == 2

    assert pattern_1.unique_key == pattern_2.unique_key


def test_default_util_pat(reset_util_pattern):
    pattern_1 = PHX.schedules.Schedule_Occupancy.default()
    pattern_2 = PHX.schedules.Schedule_Occupancy.default()

    assert pattern_1.id == 1
    assert pattern_2.id == 1

    assert pattern_1.unique_key == pattern_2.unique_key


def test_util_pat_different_values(reset_util_pattern):
    # Different Start Hour
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_1.start_hour = 1
    pattern_2 = PHX.schedules.Schedule_Occupancy()
    pattern_2.start_hour = 2

    assert pattern_1.unique_key != pattern_2.unique_key

    # Different End Hour
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_1.end_hour = 1
    pattern_2 = PHX.schedules.Schedule_Occupancy()
    pattern_2.end_hour = 2

    assert pattern_1.unique_key != pattern_2.unique_key

    # Different annual_utilization_days
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_1.annual_utilization_days = 1
    pattern_2 = PHX.schedules.Schedule_Occupancy()
    pattern_2.annual_utilization_days = 2

    assert pattern_1.unique_key != pattern_2.unique_key

    # Different annual_utilization_factor
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_1.annual_utilization_factor = 0.12
    pattern_2 = PHX.schedules.Schedule_Occupancy()
    pattern_2.annual_utilization_factor = 0.13

    assert pattern_1.unique_key != pattern_2.unique_key
