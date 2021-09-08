import PHX.utilization_patterns


def test_pattern_serialization():
    pattern_1 = PHX.utilization_patterns.UtilPat_Vent()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.UtilPat_Vent.from_dict(d)

    assert d == pattern_2.to_dict()


def test_pattern_default_serialization():
    pattern_1 = PHX.utilization_patterns.UtilPat_Vent.default()
    d = pattern_1.to_dict()
    pattern_2 = PHX.utilization_patterns.UtilPat_Vent.from_dict(d)

    assert d == pattern_2.to_dict()
