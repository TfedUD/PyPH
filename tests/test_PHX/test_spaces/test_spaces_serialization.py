import PHX.spaces


def test_FloorSegment_serialization():
    o1 = PHX.spaces.FloorSegment()
    d = o1.to_dict()

    o2 = PHX.spaces.FloorSegment.from_dict(d)

    assert d == o2.to_dict()


def test_FloorSegment_with_geom_serialization(polygon_1, polygon_2):
    o1 = PHX.spaces.FloorSegment()
    o1.geometry.append(polygon_1)
    o1.geometry.append(polygon_2)

    d = o1.to_dict()

    o2 = PHX.spaces.FloorSegment.from_dict(d)

    assert d == o2.to_dict()


def test_Floor_serialization():
    o1 = PHX.spaces.Floor()
    d = o1.to_dict()

    o2 = PHX.spaces.Floor.from_dict(d)

    assert d == o2.to_dict()


def test_Floor_with_segments_serialization():
    seg = PHX.spaces.FloorSegment()
    o1 = PHX.spaces.Floor()
    o1.add_new_floor_segment(seg)
    d = o1.to_dict()

    o2 = PHX.spaces.Floor.from_dict(d)

    assert d == o2.to_dict()


def test_Floor_with_segments_with_geometry_serialization(polygon_1):
    seg = PHX.spaces.FloorSegment()
    seg.geometry.append(polygon_1)

    o1 = PHX.spaces.Floor()
    o1.add_new_floor_segment(seg)
    d = o1.to_dict()

    o2 = PHX.spaces.Floor.from_dict(d)

    assert d == o2.to_dict()


def test_Volume_serialization():
    o1 = PHX.spaces.Volume()
    d1 = o1.to_dict()

    o2 = PHX.spaces.Volume.from_dict(d1)
    d2 = o2.to_dict()
    assert d1 == d2


def test_Volume_with_space_geometry(polygon_1):
    v1 = PHX.spaces.Volume()
    v1.volume_geometry.append([polygon_1])
    d1 = v1.to_dict()

    o2 = PHX.spaces.Volume.from_dict(d1)
    d2 = o2.to_dict()
    assert d1 == d2


def test_Space_serialization():
    o1 = PHX.spaces.Space()
    d = o1.to_dict()

    o2 = PHX.spaces.Space.from_dict(d)

    assert d == o2.to_dict()


def test_Space_with_Volumes_serialization(polygon_1):
    v1 = PHX.spaces.Volume()
    v1.volume_geometry.append([polygon_1])

    space_1 = PHX.spaces.Space()
    space_1.add_new_volume(v1)

    d1 = space_1.to_dict()

    o2 = PHX.spaces.Space.from_dict(d1)
    d2 = o2.to_dict()

    assert d1 == d2
