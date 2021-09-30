import PHX.mechanicals.systems
import PHX.mechanicals.equipment
import pytest


@pytest.fixture
def reset_mechanicals():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.mechanicals.systems.MechanicalSystem._count = 0
    PHX.mechanicals.equipment.EquipmentSet._count = 0
    PHX.mechanicals.equipment.HVAC_Device._count = 0
    PHX.mechanicals.equipment.HVAC_Ventilator._count = 0

    yield

    PHX.mechanicals.systems.MechanicalSystem._count = 0
    PHX.mechanicals.equipment.EquipmentSet._count = 0
    PHX.mechanicals.equipment.HVAC_Device._count = 0
    PHX.mechanicals.equipment.HVAC_Ventilator._count = 0
