import PHX.programs.ventilation
import pytest


@pytest.fixture
def reset_ventilation():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.programs.ventilation.RoomVentilation._count = 0

    yield

    PHX.programs.ventilation.RoomVentilation._count = 0
