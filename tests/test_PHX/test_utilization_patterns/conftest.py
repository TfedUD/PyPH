import PHX.utilization_patterns
import pytest


@pytest.fixture
def reset_util_pattern():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.utilization_patterns.UtilPat_Vent._count = 0
    PHX.utilization_patterns.UtilPat_Vent._default = None
    PHX.utilization_patterns.UtilPat_Occupancy._count = 0
    PHX.utilization_patterns.UtilPat_Occupancy._default = None
    PHX.utilization_patterns.UtilPat_Lighting._count = 0
    PHX.utilization_patterns.UtilPat_Lighting._default = None

    yield

    PHX.utilization_patterns.UtilPat_Vent._count = 0
    PHX.utilization_patterns.UtilPat_Vent._default = None
    PHX.utilization_patterns.UtilPat_Occupancy._count = 0
    PHX.utilization_patterns.UtilPat_Occupancy._default = None
    PHX.utilization_patterns.UtilPat_Lighting._count = 0
    PHX.utilization_patterns.UtilPat_Lighting._default = None
