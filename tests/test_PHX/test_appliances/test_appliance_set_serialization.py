import PHX.appliances


def test_full_set_serialization():
    s = PHX.appliances.ApplianceSet()
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Clothes_Dryer())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Clothes_Washer())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Combo_Fridge())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Cooktop())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Dishwasher())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Freezer())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Fridge())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Lighting_Ext())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Lighting_Int())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_MEL())

    d = s.to_dict()
    new_obj = PHX.appliances.ApplianceSet.from_dict(d)
    assert d == new_obj.to_dict()


def test_partial_set_serialization():
    s = PHX.appliances.ApplianceSet()
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Clothes_Washer())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Cooktop())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Freezer())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Lighting_Ext())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_MEL())

    d = s.to_dict()
    new_obj = PHX.appliances.ApplianceSet.from_dict(d)
    assert d == new_obj.to_dict()
