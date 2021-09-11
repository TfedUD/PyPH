import PHX.assemblies
import pytest


def test_Assembly_basic(reset_assembly_classes):
    a1 = PHX.assemblies.Assembly()

    assert a1
    assert isinstance(a1, PHX.assemblies.Assembly)
    assert a1.id == 1

    a2 = PHX.assemblies.Assembly()
    assert a1.id == 1
    assert a2.id == 2


def test_Assembly_add_Layer(reset_assembly_classes):
    a1 = PHX.assemblies.Assembly()
    l1 = PHX.assemblies.Layer()

    assert len(a1.Layers) == 0

    a1.add_layer(l1)

    assert len(a1.Layers) == 1
    assert l1 in a1.Layers


def test_Assembly_add_not_a_Layer(reset_assembly_classes):
    a1 = PHX.assemblies.Assembly()
    assert len(a1.Layers) == 0

    with pytest.raises(PHX.assemblies.LayerTypeError):
        a1.add_layer("Not a Layer")

    assert len(a1.Layers) == 0

    with pytest.raises(PHX.assemblies.LayerTypeError):
        a1.add_layer(None)

    assert len(a1.Layers) == 0
