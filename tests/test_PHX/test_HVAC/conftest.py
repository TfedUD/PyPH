import PHX.hvac
import pytest


@pytest.fixture
def reset_hvac():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.hvac.HVAC_Device._count = 0
    PHX.hvac.HVAC_System._count = 0

    yield

    PHX.hvac.HVAC_Device._count = 0
    PHX.hvac.HVAC_System._count = 0
