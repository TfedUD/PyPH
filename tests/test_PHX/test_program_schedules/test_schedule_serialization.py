import PHX.schedules


def test_lighting_serialization():
    pattern_1 = PHX.schedules.Schedule_Lighting()
    d = pattern_1.to_dict()
    pattern_2 = PHX.schedules.Schedule_Lighting.from_dict(d)

    assert d == pattern_2.to_dict()


def test_lighting_default_serialization():
    pattern_1 = PHX.schedules.Schedule_Lighting.default()
    d = pattern_1.to_dict()
    pattern_2 = PHX.schedules.Schedule_Lighting.from_dict(d)

    assert d == pattern_2.to_dict()


def test_occupancy_serialization():
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    d = pattern_1.to_dict()
    pattern_2 = PHX.schedules.Schedule_Occupancy.from_dict(d)

    assert d == pattern_2.to_dict()


def test_occupancy_default_serialization():
    pattern_1 = PHX.schedules.Schedule_Occupancy.default()
    d = pattern_1.to_dict()
    pattern_2 = PHX.schedules.Schedule_Occupancy.from_dict(d)

    assert d == pattern_2.to_dict()


def test_rates_serialization():
    pattern_1 = PHX.schedules.Vent_UtilRates()
    d = pattern_1.to_dict()
    pattern_2 = PHX.schedules.Vent_UtilRates.from_dict(d)

    assert d == pattern_2.to_dict()


def test_rate_serialization():
    pattern_1 = PHX.schedules.Vent_UtilRate()
    d = pattern_1.to_dict()
    pattern_2 = PHX.schedules.Vent_UtilRate.from_dict(d)

    assert d == pattern_2.to_dict()


def test_vent_serialization():
    pattern_1 = PHX.schedules.Schedule_Ventilation()
    d = pattern_1.to_dict()
    pattern_2 = PHX.schedules.Schedule_Ventilation.from_dict(d)

    assert d == pattern_2.to_dict()


def test_vent_default_serialization():
    pattern_1 = PHX.schedules.Schedule_Ventilation.default()
    d = pattern_1.to_dict()
    pattern_2 = PHX.schedules.Schedule_Ventilation.from_dict(d)

    assert d == pattern_2.to_dict()
