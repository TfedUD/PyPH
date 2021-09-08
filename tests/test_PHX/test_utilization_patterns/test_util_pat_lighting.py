import PHX.utilization_patterns


def test_util_pat(reset_util_pattern):
    pattern_1 = PHX.utilization_patterns.UtilPat_Lighting()
    pattern_2 = PHX.utilization_patterns.UtilPat_Lighting()

    assert pattern_1.id == 1
    assert pattern_2.id == 2

    assert pattern_1.unique_key == pattern_2.unique_key


def test_default_util_pat(reset_util_pattern):
    pattern_1 = PHX.utilization_patterns.UtilPat_Lighting.default()
    pattern_2 = PHX.utilization_patterns.UtilPat_Lighting.default()

    assert pattern_1.id == 1
    assert pattern_2.id == 1

    assert pattern_1.unique_key == pattern_2.unique_key


def test_util_pat_different_values(reset_util_pattern):
    pattern_1 = PHX.utilization_patterns.UtilPat_Lighting()
    pattern_1.annual_utilization_factor = 1
    pattern_2 = PHX.utilization_patterns.UtilPat_Lighting()
    pattern_2.annual_utilization_factor = 2

    assert pattern_1.id == 1
    assert pattern_2.id == 2

    assert pattern_1.unique_key != pattern_2.unique_key
