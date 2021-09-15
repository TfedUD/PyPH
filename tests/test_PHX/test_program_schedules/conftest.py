import PHX.schedules
import pytest


@pytest.fixture
def reset_schedules():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.schedules.Schedule_Ventilation._count = 0
    PHX.schedules.Schedule_Ventilation._default = None
    PHX.schedules.Schedule_Occupancy._count = 0
    PHX.schedules.Schedule_Occupancy._default = None
    PHX.schedules.Schedule_Lighting._count = 0
    PHX.schedules.Schedule_Lighting._default = None

    yield

    PHX.schedules.Schedule_Ventilation._count = 0
    PHX.schedules.Schedule_Ventilation._default = None
    PHX.schedules.Schedule_Occupancy._count = 0
    PHX.schedules.Schedule_Occupancy._default = None
    PHX.schedules.Schedule_Lighting._count = 0
    PHX.schedules.Schedule_Lighting._default = None
