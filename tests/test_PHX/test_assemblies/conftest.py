import pytest
import PHX.assemblies


@pytest.fixture
def reset_assembly_classes():
    PHX.assemblies.Material._count = 0
    PHX.assemblies.Layer._count = 0
    PHX.assemblies.Assembly._count = 0

    yield

    PHX.assemblies.Material._count = 0
    PHX.assemblies.Layer._count = 0
    PHX.assemblies.Assembly._count = 0
