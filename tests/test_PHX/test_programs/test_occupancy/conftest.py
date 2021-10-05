import PHX.programs.occupancy
import pytest


@pytest.fixture
def reset_occupancies():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.programs.occupancy.ZoneOccupancy._count = 0
    PHX.programs.occupancy.BldgSegmentOccupancy._count = 0
    PHX.programs.occupancy.RoomOccupancy._count = 0
    PHX.programs.occupancy.RoomOccupancy._default = None

    yield

    PHX.programs.occupancy.ZoneOccupancy._count = 0
    PHX.programs.occupancy.BldgSegmentOccupancy._count = 0
    PHX.programs.occupancy.RoomOccupancy._count = 0
    PHX.programs.occupancy.RoomOccupancy._default = None
