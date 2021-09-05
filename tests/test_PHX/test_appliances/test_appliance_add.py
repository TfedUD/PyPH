import PHX.appliances
import pytest


def test_add_Nones():
    app1 = PHX.appliances.Appliance()
    app2 = None

    # Works if obj_a is an Applince
    app3 = app1 + app2
    assert app1 == app3

    # Error if obj_a is NoneType
    with pytest.raises(TypeError):
        app4 = app2 + app1


def test_add_PHIUS_dishwashers():
    dw1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw1.energy_demand = 200
    dw1.dishwasher_capacity = 10
    dw2 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw2.energy_demand = 200
    dw2.dishwasher_capacity = 10

    # Add the two appliancs
    dw3 = dw1 + dw2
    assert dw3.type == 1
    assert dw3.quantity == 2
    assert dw3.energy_demand == 200
    assert dw3.dishwasher_capacity == 10

    # Add an third one
    dw4 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw4.energy_demand = 600
    dw4.dishwasher_capacity = 25

    dw5 = dw3 + dw4
    assert dw5.type == 1
    assert dw5.quantity == 3
    assert dw5.energy_demand == (200 + 200 + 600) / 3
    assert dw5.dishwasher_capacity == (10 + 10 + 25) / 3


def test_add_dw_and_not_dw():
    dw1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    cktp = PHX.appliances.Appliance.PHIUS_Cooktop()

    with pytest.raises(PHX.appliances.ApplianceAdditionError):
        dw1 + cktp
