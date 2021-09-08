import PHX.ground


def test_lighting_serialization():
    pattern_1 = PHX.ground.Foundation()
    d = pattern_1.to_dict()
    pattern_2 = PHX.ground.Foundation.from_dict(d)

    assert d == pattern_2.to_dict()
