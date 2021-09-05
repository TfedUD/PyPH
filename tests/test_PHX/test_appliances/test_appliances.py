import PHX.appliances


def test_appliances():
    a1 = PHX.appliances.Appliance()
    assert a1

    dw = PHX.appliances.Appliance.PHIUS_Dishwasher()
    assert dw.type == 1

    wsh = PHX.appliances.Appliance.PHIUS_Clothes_Washer()
    assert wsh.type == 2

    dry = PHX.appliances.Appliance.PHIUS_Clothes_Dryer()
    assert dry.type == 3

    cook = PHX.appliances.Appliance.PHIUS_Cooktop()
    assert cook.type == 7

    fr = PHX.appliances.Appliance.PHIUS_Fridge()
    assert fr.type == 4

    frz = PHX.appliances.Appliance.PHIUS_Freezer()
    assert frz.type == 5

    f = PHX.appliances.Appliance.PHIUS_Combo_Fridge()
    assert f.type == 6

    f = PHX.appliances.Appliance.PHIUS_Lighting_Int()
    assert f.type == 14

    f = PHX.appliances.Appliance.PHIUS_Lighting_Ext()
    assert f.type == 15

    f = PHX.appliances.Appliance.PHIUS_MEL()
    assert f.type == 13


def test_PHIUS_MEL():
    # -- Don't set any values
    mel = PHX.appliances.Appliance.PHIUS_MEL()
    assert not mel.energy_demand
    assert not mel.energy_demand_per_use
    assert not mel.combined_energy_facor

    # -- Set the energy values
    mel2 = PHX.appliances.Appliance.PHIUS_MEL(
        energy_demand=123,
        energy_demand_per_use=456,
        combined_energy_facor=789,
    )
    assert mel2.energy_demand == 123
    assert mel2.energy_demand_per_use == 456
    assert mel2.combined_energy_facor == 789

    # -- Only set 2 of them
    mel3 = PHX.appliances.Appliance.PHIUS_MEL(
        energy_demand=123,
        energy_demand_per_use=456,
    )
    assert mel3.energy_demand == 123
    assert mel3.energy_demand_per_use == 456
    assert mel3.combined_energy_facor == 0


def test_PHIUS_Lighting_Int():
    # -- Don't set any values
    a = PHX.appliances.Appliance.PHIUS_Lighting_Int()
    assert not a.energy_demand
    assert not a.energy_demand_per_use
    assert not a.combined_energy_facor

    # -- Set the energy values
    a_2 = PHX.appliances.Appliance.PHIUS_Lighting_Int(
        energy_demand=123,
        energy_demand_per_use=456,
        combined_energy_facor=789,
    )
    assert a_2.energy_demand == 123
    assert a_2.energy_demand_per_use == 456
    assert a_2.combined_energy_facor == 789

    # -- Only set 2 of them
    a_3 = PHX.appliances.Appliance.PHIUS_Lighting_Int(
        energy_demand=123,
        energy_demand_per_use=456,
    )
    assert a_3.energy_demand == 123
    assert a_3.energy_demand_per_use == 456
    assert a_3.combined_energy_facor == 0


def test_PHIUS_Lighting_Ext():
    # -- Don't set any values
    a = PHX.appliances.Appliance.PHIUS_Lighting_Ext()
    assert not a.energy_demand
    assert not a.energy_demand_per_use
    assert not a.combined_energy_facor

    # -- Set the energy values
    a_2 = PHX.appliances.Appliance.PHIUS_Lighting_Ext(
        energy_demand=123,
        energy_demand_per_use=456,
        combined_energy_facor=789,
    )
    assert a_2.energy_demand == 123
    assert a_2.energy_demand_per_use == 456
    assert a_2.combined_energy_facor == 789

    # -- Only set 2 of them
    a_3 = PHX.appliances.Appliance.PHIUS_Lighting_Ext(
        energy_demand=123,
        energy_demand_per_use=456,
    )
    assert a_3.energy_demand == 123
    assert a_3.energy_demand_per_use == 456
    assert a_3.combined_energy_facor == 0
