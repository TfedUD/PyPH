import PHX.assemblies
import pytest


def test_Layer_basic(reset_assembly_classes):
    l1 = PHX.assemblies.Layer()

    assert l1
    assert isinstance(l1, PHX.assemblies.Layer)
    assert l1.id == 1

    l2 = PHX.assemblies.Layer()
    assert l1.id == 1
    assert l2.id == 2


def test_Layer_set_material(reset_assembly_classes):
    l = PHX.assemblies.Layer()
    m = PHX.assemblies.Material()

    l.material = m


def test_Layer_set_not_a_material(reset_assembly_classes):
    l = PHX.assemblies.Layer()

    m = "Not a Material"
    with pytest.raises(PHX.assemblies.MaterialTypeError):
        l.material = m

    m = None
    with pytest.raises(PHX.assemblies.MaterialTypeError):
        l.material = m
