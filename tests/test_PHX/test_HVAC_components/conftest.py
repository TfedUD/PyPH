import PHX.hvac_components
import PHX.hvac_system
import pytest


@pytest.fixture
def reset_vent_components():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.hvac_components.HVAC_Duct_Segment._default = None
    PHX.hvac_components.HVAC_Duct._default = None
    PHX.hvac_components.HVAC_Ventilator._default = None
    PHX.hvac_components.HVAC_Ventilator._count = 0
    PHX.hvac_system.HVAC_System._count = 0

    yield

    PHX.hvac_components.HVAC_Duct_Segment._default = None
    PHX.hvac_components.HVAC_Duct._default = None
    PHX.hvac_components.HVAC_Ventilator._default = None
    PHX.hvac_components.HVAC_Ventilator._count = 0
    PHX.hvac_system.HVAC_System._count = 0
