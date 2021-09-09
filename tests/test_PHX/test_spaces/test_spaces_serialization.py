import PHX.spaces


def test_FloorSegment_serialization():
    o1 = PHX.spaces.FloorSegment()
    d = o1.to_dict()

    o2 = PHX.spaces.FloorSegment.from_dict(d)

    assert d == o2.to_dict()


def test_Floor_serialization():
    o1 = PHX.spaces.Floor()
    d = o1.to_dict()

    o2 = PHX.spaces.Floor.from_dict(d)

    assert d == o2.to_dict()


def test_Volume_serialization():
    o1 = PHX.spaces.Volume()
    d1 = o1.to_dict()

    o2 = PHX.spaces.Volume.from_dict(d1)
    d2 = o2.to_dict()
    assert d1 == d2


def test_Space_serialization():
    o1 = PHX.spaces.Space()
    d = o1.to_dict()

    o2 = PHX.spaces.Space.from_dict(d)

    assert d == o2.to_dict()
