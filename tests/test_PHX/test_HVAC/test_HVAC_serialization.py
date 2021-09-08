import PHX.hvac


def test_hvac_system_serialization():
    pattern_1 = PHX.hvac.HVAC_System()
    d = pattern_1.to_dict()
    pattern_2 = PHX.hvac.HVAC_System.from_dict(d)

    assert d == pattern_2.to_dict()
