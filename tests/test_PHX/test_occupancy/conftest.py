import PHX.occupancy
import pytest


@pytest.fixture
def reset_occupancies():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.occupancy.ZoneOccupancy._count = 0
    PHX.occupancy.BldgSegmentOccupancy._count = 0
    PHX.occupancy.SpaceOccupancy._count = 0
    PHX.occupancy.SpaceOccupancy._default = None

    yield

    PHX.occupancy.ZoneOccupancy._count = 0
    PHX.occupancy.BldgSegmentOccupancy._count = 0
    PHX.occupancy.SpaceOccupancy._count = 0
    PHX.occupancy.SpaceOccupancy._default = None
