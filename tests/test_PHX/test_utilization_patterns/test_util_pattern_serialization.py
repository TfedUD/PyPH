import PHX.utilization_patterns


def test_lighting_serialization():
    pattern_1 = PHX.utilization_patterns.UtilPat_Lighting()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.UtilPat_Lighting.from_dict(d)

    assert d == pattern_2.to_dict()


def test_lighting_default_serialization():
    pattern_1 = PHX.utilization_patterns.UtilPat_Lighting.default()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.UtilPat_Lighting.from_dict(d)

    assert d == pattern_2.to_dict()


def test_occupancy_serialization():
    pattern_1 = PHX.utilization_patterns.UtilPat_Occupancy()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.UtilPat_Occupancy.from_dict(d)

    assert d == pattern_2.to_dict()


def test_occupancy_default_serialization():
    pattern_1 = PHX.utilization_patterns.UtilPat_Occupancy.default()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.UtilPat_Occupancy.from_dict(d)

    assert d == pattern_2.to_dict()


def test_rates_serialization():
    pattern_1 = PHX.utilization_patterns.Vent_UtilRates()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.Vent_UtilRates.from_dict(d)

    assert d == pattern_2.to_dict()


def test_rate_serialization():
    pattern_1 = PHX.utilization_patterns.Vent_UtilRate()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.Vent_UtilRate.from_dict(d)

    assert d == pattern_2.to_dict()


def test_vent_serialization():
    pattern_1 = PHX.utilization_patterns.UtilPat_Vent()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.UtilPat_Vent.from_dict(d)

    assert d == pattern_2.to_dict()


def test_vent_default_serialization():
    pattern_1 = PHX.utilization_patterns.UtilPat_Vent.default()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.UtilPat_Vent.from_dict(d)

    assert d == pattern_2.to_dict()
