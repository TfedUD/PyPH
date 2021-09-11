import PHX.assemblies


def test_Material_basic(reset_assembly_classes):
    m1 = PHX.assemblies.Material()

    assert m1
    assert isinstance(m1, PHX.assemblies.Material)
    assert m1.id == 1

    m2 = PHX.assemblies.Material()
    assert m1.id == 1
    assert m2.id == 2
