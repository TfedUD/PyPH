import PHX.ventilation_components
import pytest


@pytest.fixture
def reset_vent_components():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.ventilation_components.Ventilation_Duct_Segment._default = None
    PHX.ventilation_components.Ventilation_Duct._default = None
    PHX.ventilation_components.Ventilator._default = None
    PHX.ventilation_components.Ventilator._count = 0
    PHX.ventilation_components.Ventilation_System._default = None
    PHX.ventilation_components.Ventilation_System._count = 0

    yield

    PHX.ventilation_components.Ventilation_Duct_Segment._default = None
    PHX.ventilation_components.Ventilation_Duct._default = None
    PHX.ventilation_components.Ventilator._default = None
    PHX.ventilation_components.Ventilator._count = 0
    PHX.ventilation_components.Ventilation_System._default = None
    PHX.ventilation_components.Ventilation_System._count = 0
