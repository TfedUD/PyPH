import PHX.hvac_system
import pytest


@pytest.fixture
def reset_hvac():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.hvac_components.HVAC_Device._count = 0
    PHX.hvac_system.HVAC_System._count = 0

    yield

    PHX.hvac_components.HVAC_Device._count = 0
    PHX.hvac_system.HVAC_System._count = 0
