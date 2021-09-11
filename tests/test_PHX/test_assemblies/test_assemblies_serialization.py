import PHX.assemblies


def test_Material_serialization():
    o1 = PHX.assemblies.Material()
    d = o1.to_dict()

    o2 = PHX.assemblies.Material.from_dict(d)

    assert d == o2.to_dict()


def test_Layer_serialization():
    o1 = PHX.assemblies.Layer()
    d = o1.to_dict()

    o2 = PHX.assemblies.Material.from_dict(d)

    assert d == o2.to_dict()


def test_Assembly_serialization():
    o1 = PHX.assemblies.Assembly()
    d = o1.to_dict()

    o2 = PHX.assemblies.Material.from_dict(d)

    assert d == o2.to_dict()
