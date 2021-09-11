import PHX.appliances
import pytest


def test_add_appliance_to_set():
    s = PHX.appliances.ApplianceSet()
    assert len(s) == 0

    # Add New
    app_1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    s.add_appliances_to_set(app_1)
    assert len(s) == 1

    # Add New
    app_2 = PHX.appliances.Appliance.PHIUS_Clothes_Dryer()
    s.add_appliances_to_set(app_2)
    assert len(s) == 2

    app = PHX.appliances.Appliance.PHIUS_Clothes_Washer()
    s.add_appliances_to_set(app)
    assert len(s) == 3

    app = PHX.appliances.Appliance.PHIUS_Combo_Fridge()
    s.add_appliances_to_set(app)
    assert len(s) == 4

    app = PHX.appliances.Appliance.PHIUS_Cooktop()
    s.add_appliances_to_set(app)
    assert len(s) == 5

    app = PHX.appliances.Appliance.PHIUS_Freezer()
    s.add_appliances_to_set(app)
    assert len(s) == 6

    app = PHX.appliances.Appliance.PHIUS_Fridge()
    s.add_appliances_to_set(app)
    assert len(s) == 7

    app = PHX.appliances.Appliance.PHIUS_Lighting_Ext()
    s.add_appliances_to_set(app)
    assert len(s) == 8

    app = PHX.appliances.Appliance.PHIUS_Lighting_Int()
    s.add_appliances_to_set(app)
    assert len(s) == 9

    app = PHX.appliances.Appliance.PHIUS_MEL()
    s.add_appliances_to_set(app)
    assert len(s) == 10

    # Add Same
    app_3 = PHX.appliances.Appliance.PHIUS_Clothes_Dryer()
    s.add_appliances_to_set(app_3)
    assert len(s) == 11


def test_add_not_an_appliance():
    s = PHX.appliances.ApplianceSet()
    assert len(s) == 0

    app_1 = PHX.appliances.Appliance()
    app_1.type = 999_999
    with pytest.raises(PHX.appliances.UnknownApplianceError):
        s.add_appliances_to_set(app_1)
    assert len(s) == 0

    not_app = None
    s.add_appliances_to_set(not_app)
    assert len(s) == 0


def test_full_set_iteration():
    s = PHX.appliances.ApplianceSet()
    assert len(s) == 0

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

    assert len(s) == 10
    for app in s:
        assert isinstance(app, PHX.appliances.Appliance)


def test_partial_set_iteration():
    s = PHX.appliances.ApplianceSet()
    assert len(s) == 0

    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Clothes_Washer())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Fridge())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Combo_Fridge())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_MEL())
    s.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Lighting_Ext())

    assert len(s) == 5

    _types = {2, 4, 6, 13, 15}
    for app, _type in zip(s, _types):
        assert app.type == _type
