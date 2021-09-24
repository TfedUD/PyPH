import PHX.ventilation
import pytest


@pytest.fixture
def reset_ventilation():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.ventilation.SpaceVentilation._count = 0

    yield

    PHX.ventilation.SpaceVentilation._count = 0
