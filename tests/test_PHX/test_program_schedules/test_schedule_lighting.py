import PHX.programs.schedules


def test_util_pat(reset_schedules):
    pattern_1 = PHX.programs.schedules.Schedule_Lighting()
    pattern_2 = PHX.programs.schedules.Schedule_Lighting()

    assert pattern_1.id == 1
    assert pattern_2.id == 2

    assert pattern_1.unique_key == pattern_2.unique_key


def test_default_util_pat(reset_schedules):
    pattern_1 = PHX.programs.schedules.Schedule_Lighting.default()
    pattern_2 = PHX.programs.schedules.Schedule_Lighting.default()

    assert pattern_1.id == 1
    assert pattern_2.id == 1

    assert pattern_1.unique_key == pattern_2.unique_key


def test_util_pat_different_values(reset_schedules):
    pattern_1 = PHX.programs.schedules.Schedule_Lighting()
    pattern_1.annual_utilization_factor = 1
    pattern_2 = PHX.programs.schedules.Schedule_Lighting()
    pattern_2.annual_utilization_factor = 2

    assert pattern_1.id == 1
    assert pattern_2.id == 2

    assert pattern_1.unique_key != pattern_2.unique_key
