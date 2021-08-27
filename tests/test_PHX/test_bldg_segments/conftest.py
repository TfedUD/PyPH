import pytest
import PHX.bldg_segment


@pytest.fixture
def reset_bldg_segment_count():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.bldg_segment.Zone._count = 0
    PHX.bldg_segment.BldgSegment._count = 0

    yield

    PHX.bldg_segment.Zone._count = 0
    PHX.bldg_segment.BldgSegment._count = 0
