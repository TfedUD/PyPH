import PHX.programs.lighting


def test_default_lighting_serialization():
    l1 = PHX.programs.lighting.RoomLighting.default()

    d = l1.to_dict()
    print(d)
    l2 = PHX.programs.lighting.RoomLighting.from_dict(d)

    assert d == l2.to_dict()


def test_lighting_serialization():
    l1 = PHX.programs.lighting.RoomLighting.default()
    l1.name = "custom name"
    l1.loads.target_lux = 12345
    l1.loads.watts_per_area = 0.12346

    d = l1.to_dict()
    l2 = PHX.programs.lighting.RoomLighting.from_dict(d)

    assert d == l2.to_dict()
